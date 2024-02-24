import logging
import os
import smtplib
from email.message import EmailMessage
from pathlib import Path
from secrets import token_urlsafe
from typing import Literal

from PIL import Image
from celery import shared_task
from flask import url_for
from werkzeug.datastructures import FileStorage

from src.config import EMAIL_SENDER, EMAIL_HOST, EMAIL_PORT, EMAIL_USERNAME, EMAIL_PASSWORD, BASE_DIR


class PictureService:
    @staticmethod
    def generate_rel_pic_path(img_catalog: Literal['postimg', 'userimg'], filename: str) -> str:
        _, ext = os.path.splitext(filename)
        pic_name = token_urlsafe(16) + ext
        return url_for('static', filename=f'img/{img_catalog}/{pic_name}')

    @staticmethod
    def generate_abs_pic_path(rel_pic_path: str | os.PathLike[str]) -> Path:
        return BASE_DIR / rel_pic_path[1:]

    def save_picture(self,
                     pic_file: FileStorage,
                     rel_pic_path: str | os.PathLike[str],
                     pic_size: tuple[int, int]) -> None:
        abs_pic_path = self.generate_abs_pic_path(rel_pic_path=rel_pic_path)

        with Image.open(pic_file) as img:
            img = img.convert(mode='RGB')
            img = img.resize(size=pic_size)
            img.save(fp=abs_pic_path)

    def delete_picture(self, rel_pic_path: str | os.PathLike[str]) -> None:
        if rel_pic_path.endswith('default.jpg'):
            return

        abs_pic_path = self.generate_abs_pic_path(rel_pic_path=rel_pic_path)
        try:
            os.remove(abs_pic_path)
        except FileNotFoundError:
            logging.warning('Attempt to delete a non-existent file: %s', rel_pic_path)


class EmailService:
    @staticmethod
    @shared_task
    def send_email(email_subject: str, email_receivers: list[str], email_body: str) -> None:
        email = EmailMessage()
        email['Subject'] = email_subject
        email['From'] = EMAIL_SENDER
        email['To'] = email_receivers
        email.set_content(email_body, subtype='html')

        try:
            with smtplib.SMTP_SSL(host=EMAIL_HOST, port=EMAIL_PORT) as server:
                server.login(user=EMAIL_USERNAME, password=EMAIL_PASSWORD)
                server.send_message(email)
        except smtplib.SMTPServerDisconnected:
            logging.warning('SMTP server has unexpectedly disconnected')
