import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv('PORT'))
DEBUG = bool(os.getenv('DEBUG'))

BASE_DIR = Path(__file__).parent

PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_HOST = os.getenv('PG_HOST')
PG_PORT = os.getenv('PG_PORT')
PG_DB = os.getenv('PG_DB')

PG_USER_TEST = os.getenv('PG_USER_TEST')
PG_PASSWORD_TEST = os.getenv('PG_PASSWORD_TEST')
PG_HOST_TEST = os.getenv('PG_HOST_TEST')
PG_PORT_TEST = os.getenv('PG_PORT_TEST')
PG_DB_TEST = os.getenv('PG_DB_TEST')

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')

RESET_PSW_TOKEN_EXPIRES = int(os.getenv('RESET_PSW_TOKEN_EXPIRES'))

EMAIL_HOST = os.getenv('EMAIL_SMTP_SERVER')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
TEST_EMAIL_RECEIVER = os.getenv('TEST_EMAIL_RECEIVER')


class DevelopmentSettings:
    DEBUG = True
    TESTING = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}'
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_size': 10,
                                 'pool_recycle': 3600,
                                 'pool_pre_ping': True}
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WTF_CSRF_SECRET_KEY = os.getenv('CSRF_SECRET_KEY')
    WTF_CSRF_TIME_LIMIT = 60 * int(os.getenv('CSRF_TIME_LIMIT'))

    RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')
    RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}

    FLASK_ADMIN_SWATCH = 'cosmo'

    CELERY = {'broker_url': f'redis://{REDIS_HOST}:{REDIS_PORT}',
              'result_backend': f'redis://{REDIS_HOST}:{REDIS_PORT}',
              'task_ignore_result': True}


class TestSettings(DevelopmentSettings):
    WTF_CSRF_ENABLED = False
    LOGIN_DISABLED = True
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{PG_USER_TEST}:{PG_PASSWORD_TEST}@{PG_HOST_TEST}:{PG_PORT_TEST}/{PG_DB_TEST}'


class ProductionSettings(DevelopmentSettings):
    DEBUG = False
    TESTING = False
