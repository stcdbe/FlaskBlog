import os

from dotenv import load_dotenv


load_dotenv()

PORT = int(os.getenv("PORT"))

PGUSER = str(os.getenv("PGUSER"))
PGPASSWORD = str(os.getenv("PGPASSWORD"))
PGHOST = str(os.getenv("PGHOST"))
PGPORT = str(os.getenv("PGPORT"))
PGDB = str(os.getenv("PGDB"))


class DevelopmentConfig(object):
    DEBUG = True
    TESTING = True
    SECRET_KEY = str(os.getenv("SECRETKEY"))
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDB}'
    # SQLALCHEMY_DATABASE_URI = "sqlite:///flaskblog.db"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_size': 10,
                                 'pool_recycle': 3600,
                                 'pool_pre_ping': True}

    WTF_CSRF_SECRET_KEY = str(os.getenv("CSRFSECRETKEY"))
    WTF_CSRF_TIME_LIMIT = 3600 * 3

    RECAPTCHA_PUBLIC_KEY = str(os.getenv("RECAPTCHAPUBLICKEY"))
    RECAPTCHA_PRIVATE_KEY = str(os.getenv("RECAPTCHAPRIVATEKEY"))
    RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}

    FLASK_ADMIN_SWATCH = 'cosmo'

    EMAIL_HOST = str(os.getenv("EMAILSMTPSERVER"))
    EMAIL_PORT = int(os.getenv("EMAILPORT"))
    EMAIL_USERNAME = str(os.getenv("EMAIL"))
    EMAIL_PASSWORD = str(os.getenv("EMAILPASSWORD"))
    EMAIL_SENDER = 'noreply@flaskblog.com'


class ProductionConfig(DevelopmentConfig):
    DEBUG = False
    TESTING = False
