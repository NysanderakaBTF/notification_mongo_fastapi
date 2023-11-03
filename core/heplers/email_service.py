from email.message import EmailMessage

import aiosmtplib
from email_validator import validate_email, EmailNotValidError
from fastapi import HTTPException

from core.config.env_config import config


class EmailService:
    @staticmethod
    async def send_email(text, to):
        """Send email using the specified smtp credentials in environment"""
        smtp = aiosmtplib.SMTP()
        await smtp.connect(hostname=config.SMTP_HOST, port=config.SMTP_PORT)
        await smtp.login(config.SMTP_LOGIN, config.SMTP_PASSWORD)

        message = EmailMessage()
        message['From'] = config.SMTP_EMAIL
        message['Subject'] = 'Notification'
        message['To'] = to
        message.set_content(text)
        await smtp.send_message(message)
        await smtp.quit()

    @staticmethod
    def check_email(email):
        """validate email"""
        try:
            v = validate_email(email)
            return v["email"]
        except EmailNotValidError as e:
            raise HTTPException(status_code=400, detail=str(e))
