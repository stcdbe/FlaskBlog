import logging
import smtplib
from email.message import EmailMessage

from celery import shared_task

from src.config import env


class SMTPEmailSender:
    @staticmethod
    @shared_task
    def send_email(email_subject: str, email_receivers: list[str], email_body: str) -> None:
        email = EmailMessage()
        email["Subject"] = email_subject
        email["From"] = env.EMAIL_SENDER
        email["To"] = email_receivers
        email.set_content(email_body, subtype="html")

        try:
            with smtplib.SMTP_SSL(host=env.EMAIL_HOST, port=env.EMAIL_PORT) as server:
                server.login(user=env.EMAIL_USERNAME, password=env.EMAIL_PASSWORD)
                server.send_message(email)
        except smtplib.SMTPServerDisconnected:
            logging.warning("SMTP server has unexpectedly disconnected")
