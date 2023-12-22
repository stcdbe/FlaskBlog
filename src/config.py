from dotenv import dotenv_values


env = dotenv_values()

PORT = int(env['PORT'])

PG_USER = env['PG_USER']
PG_PASSWORD = env['PG_PASSWORD']
PG_HOST = env['PG_HOST']
PG_PORT = env['PG_PORT']
PG_DB = env['PG_DB']

RESET_PSW_TOKEN_EXPIRES = int(env['RESET_PSW_TOKEN_EXPIRES'])

EMAIL_HOST = env['EMAIL_SMTP_SERVER']
EMAIL_PORT = int(env['EMAIL_PORT'])
EMAIL_USERNAME = env['EMAIL_USERNAME']
EMAIL_PASSWORD = env['EMAIL_PASSWORD']
EMAIL_SENDER = env['EMAIL_SENDER']


class DevelopmentConfig(object):
    DEBUG = True
    TESTING = True
    SECRET_KEY = env['SECRET_KEY']
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_size': 10,
                                 'pool_recycle': 3600,
                                 'pool_pre_ping': True}

    WTF_CSRF_SECRET_KEY = env['CSRF_SECRET_KEY']
    WTF_CSRF_TIME_LIMIT = 60 * int(env['CSRF_TIME_LIMIT'])

    RECAPTCHA_PUBLIC_KEY = env['RECAPTCHA_PUBLIC_KEY']
    RECAPTCHA_PRIVATE_KEY = env['RECAPTCHA_PRIVATE_KEY']
    RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}

    FLASK_ADMIN_SWATCH = 'cosmo'


class ProductionConfig(DevelopmentConfig):
    DEBUG = False
    TESTING = False
