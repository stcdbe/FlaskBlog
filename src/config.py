import os

from dotenv import load_dotenv


load_dotenv()

PORT = int(os.getenv('PORT'))

PG_USER = str(os.getenv('PG_USER'))
PG_PASSWORD = str(os.getenv('PG_PASSWORD'))
PG_HOST = str(os.getenv('PG_HOST'))
PG_PORT = str(os.getenv('PG_PORT'))
PG_DB = str(os.getenv('PG_DB'))

RESET_PSW_TOKEN_EXPIRES = int(os.getenv('RESET_PSW_TOKEN_EXPIRES'))


class DevelopmentConfig(object):
    DEBUG = True
    TESTING = True
    SECRET_KEY = str(os.getenv('SECRET_KEY'))
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_size': 10,
                                 'pool_recycle': 3600,
                                 'pool_pre_ping': True}

    WTF_CSRF_SECRET_KEY = str(os.getenv('CSRF_SECRET_KEY'))
    WTF_CSRF_TIME_LIMIT = 3600 * 3

    RECAPTCHA_PUBLIC_KEY = str(os.getenv('RECAPTCHA_PUBLIC_KEY'))
    RECAPTCHA_PRIVATE_KEY = str(os.getenv('RECAPTCHA_PRIVATE_KEY'))
    RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}

    FLASK_ADMIN_SWATCH = 'cosmo'

    EMAIL_HOST = str(os.getenv('EMAIL_SMTP_SERVER'))
    EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
    EMAIL_USERNAME = str(os.getenv('EMAIL_USERNAME'))
    EMAIL_PASSWORD = str(os.getenv('EMAIL_PASSWORD'))
    EMAIL_SENDER = 'noreply@flaskblog.com'


class ProductionConfig(DevelopmentConfig):
    DEBUG = False
    TESTING = False
