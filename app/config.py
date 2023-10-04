import os

from dotenv import load_dotenv


load_dotenv()

PORT = int(os.getenv("PORT"))
SECRETKEY = str(os.getenv("SECRETKEY"))
CSRFSECRETKEY = str(os.getenv("CSRFSECRETKEY"))

PGUSER = str(os.getenv("PGUSER"))
PGPASSWORD = str(os.getenv("PGPASSWORD"))
PGHOST = str(os.getenv("PGHOST"))
PGPORT = str(os.getenv("PGPORT"))
PGDB = str(os.getenv("PGDB"))

RECAPTCHAPUBLICKEY = str(os.getenv("RECAPTCHAPUBLICKEY"))
RECAPTCHAPRIVATEKEY = str(os.getenv("RECAPTCHAPRIVATEKEY"))

EMAILSMTPSERVER = str(os.getenv("EMAILSMTPSERVER"))
EMAILPORT = int(os.getenv("EMAILPORT"))
EMAIL = str(os.getenv("EMAIL"))
EMAILPASSWORD = str(os.getenv("EMAILPASSWORD"))


class DevelopmentConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = SECRETKEY
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDB}'
    # SQLALCHEMY_DATABASE_URI = "sqlite:///flaskblog.db"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_size': 10,
                                 'pool_recycle': 3600,
                                 'pool_pre_ping': True}

    WTF_CSRF_SECRET_KEY = CSRFSECRETKEY
    WTF_CSRF_TIME_LIMIT = 3600 * 3

    RECAPTCHA_PUBLIC_KEY = RECAPTCHAPUBLICKEY
    RECAPTCHA_PRIVATE_KEY = RECAPTCHAPRIVATEKEY
    RECAPTCHA_DATA_ATTRS = dict(theme='dark')

    FLASK_ADMIN_SWATCH = 'cosmo'

    EMAIL_HOST = EMAILSMTPSERVER
    EMAIL_PORT = EMAILPORT
    EMAIL_USERNAME = EMAIL
    EMAIL_PASSWORD = EMAILPASSWORD
    EMAIL_SENDER = 'noreply@flaskblog.com'


class ProductionConfig(DevelopmentConfig):
    DEBUG = False
    TESTING = False
