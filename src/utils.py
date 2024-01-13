import logging
import os
import smtplib
from email.message import EmailMessage
from pathlib import Path
from secrets import token_urlsafe

from PIL import Image
from celery import shared_task
from werkzeug.datastructures.file_storage import FileStorage

from src.config import EMAIL_SENDER, EMAIL_HOST, EMAIL_PORT, EMAIL_PASSWORD, EMAIL_USERNAME


def save_picture(picture: FileStorage,
                 img_catalog: str,
                 img_size: tuple[int, int]) -> str:
    _, ext = os.path.splitext(picture.filename)
    pic_name = token_urlsafe(16) + ext
    pic_link = (Path(__file__).parent / 'static' / 'img' / img_catalog / pic_name)
    with Image.open(picture) as img:
        rgb_img = img.convert(mode='RGB')
        resized_img = rgb_img.resize(size=img_size)
        resized_img.save(fp=pic_link)
    return pic_name


def delete_picture(img_catalog: str, pic_name: str) -> None:
    if pic_name == 'default.jpg':
        return
    pic_link = (Path(__file__).parent / 'static' / 'img' / img_catalog / pic_name)
    try:
        os.remove(pic_link)
    except FileNotFoundError:
        logging.warning('Attempt to delete a non-existent file: %s', pic_link)


def create_email(email_subject: str,
                 email_receivers: list[str],
                 email_body: str) -> EmailMessage:
    email = EmailMessage()
    email['Subject'] = email_subject
    email['From'] = EMAIL_SENDER
    email['To'] = email_receivers
    email.set_content(email_body, subtype='html')
    return email


@shared_task
def send_email(email_subject: str,
               email_receivers: list[str],
               email_body: str) -> None:
    email = create_email(email_subject=email_subject,
                         email_receivers=email_receivers,
                         email_body=email_body)
    try:
        with smtplib.SMTP_SSL(host=EMAIL_HOST, port=EMAIL_PORT) as server:
            server.login(user=EMAIL_USERNAME, password=EMAIL_PASSWORD)
            server.send_message(email)
    except smtplib.SMTPServerDisconnected:
        logging.warning('SMTP server has unexpectedly disconnected')
