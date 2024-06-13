from src.config.enviroment import env


class DevelopmentSettings:
    DEBUG = True
    TESTING = True
    SECRET_KEY = env.SECRET_KEY
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    SQLALCHEMY_DATABASE_URI = env.PG_URL
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_recycle": 3600,
        "pool_pre_ping": True,
    }
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WTF_CSRF_SECRET_KEY = env.CSRF_SECRET_KEY
    WTF_CSRF_TIME_LIMIT = env.CSRF_TIME_LIMIT

    RECAPTCHA_PUBLIC_KEY = env.RECAPTCHA_PUBLIC_KEY
    RECAPTCHA_PRIVATE_KEY = env.RECAPTCHA_PRIVATE_KEY
    RECAPTCHA_DATA_ATTRS = {"theme": "dark"}

    FLASK_ADMIN_SWATCH = "cosmo"

    CELERY = {
        "broker_url": env.REDIS_URL,
        "result_backend": env.REDIS_URL,
        "task_ignore_result": True,
    }


class TestSettings(DevelopmentSettings):
    WTF_CSRF_ENABLED = False
    LOGIN_DISABLED = True
    SQLALCHEMY_DATABASE_URI = env.PG_URL_TEST


class ProductionSettings(DevelopmentSettings):
    DEBUG = False
    TESTING = False
