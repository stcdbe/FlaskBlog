import logging
import smtplib
from email.message import EmailMessage

from celery import shared_task

from src.config import EMAIL_HOST, EMAIL_PASSWORD, EMAIL_PORT, EMAIL_SENDER, EMAIL_USERNAME


class SMTPEmailSender:
    @staticmethod
    @shared_task
    def send_email(email_subject: str, email_receivers: list[str], email_body: str) -> None:
        email = EmailMessage()
        email["Subject"] = email_subject
        email["From"] = EMAIL_SENDER
        email["To"] = email_receivers
        email.set_content(email_body, subtype="html")

        try:
            with smtplib.SMTP_SSL(host=EMAIL_HOST, port=EMAIL_PORT) as server:
                server.login(user=EMAIL_USERNAME, password=EMAIL_PASSWORD)
                server.send_message(email)
        except smtplib.SMTPServerDisconnected:
            logging.warning("SMTP server has unexpectedly disconnected")
