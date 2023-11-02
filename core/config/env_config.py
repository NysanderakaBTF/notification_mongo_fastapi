import os

from pydantic import BaseConfig


class Config(BaseConfig):
    APP_PORT = int(os.getenv("PORT"))
    EMAIL = os.getenv("EMAIL")
    DB_URI = os.getenv("DB_URI")
    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT"))
    SMTP_LOGIN = os.getenv("SMTP_LOGIN")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    SMTP_EMAIL = os.getenv("SMTP_EMAIL")
    SMTP_NAME = os.getenv("SMTP_NAME")


config = Config()
