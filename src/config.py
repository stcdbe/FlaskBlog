import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(kw_only=True, frozen=True)
class Env:
    PORT: int = int(os.getenv("PORT", 5000))
    DEBUG: bool = bool(os.getenv("DEBUG", False))
    BASE_DIR: Path = Path(__file__).parent.parent
    SECRET_KEY: str = os.getenv("SECRET_KEY")

    CSRF_SECRET_KEY: str = os.getenv("CSRF_SECRET_KEY")
    CSRF_TIME_LIMIT: int = 60 * int(os.getenv("CSRF_TIME_LIMIT"))

    RECAPTCHA_PUBLIC_KEY: str = os.getenv("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY: str = os.getenv("RECAPTCHA_PRIVATE_KEY")

    _PG_URL: str = "postgresql+psycopg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

    PG_USER: str = os.getenv("PG_USER")
    PG_PASSWORD: str = os.getenv("PG_PASSWORD")
    PG_HOST: str = os.getenv("PG_HOST")
    PG_PORT: str = os.getenv("PG_PORT")
    PG_DB: str = os.getenv("PG_DB")

    PG_USER_TEST: str = os.getenv("PG_USER_TEST")
    PG_PASSWORD_TEST: str = os.getenv("PG_PASSWORD_TEST")
    PG_HOST_TEST: str = os.getenv("PG_HOST_TEST")
    PG_PORT_TEST: str = os.getenv("PG_PORT_TEST")
    PG_DB_TEST: str = os.getenv("PG_DB_TEST")

    @property
    def PG_URL(self) -> str:
        return self._PG_URL.format(
            PG_USER=self.PG_USER,
            PG_PASSWORD=self.PG_PASSWORD,
            PG_HOST=self.PG_HOST,
            PG_PORT=self.PG_PORT,
            PG_DB=self.PG_DB,
        )

    @property
    def PG_URL_TEST(self) -> str:
        return self._PG_URL.format(
            PG_USER=self.PG_USER_TEST,
            PG_PASSWORD=self.PG_PASSWORD_TEST,
            PG_HOST=self.PG_HOST_TEST,
            PG_PORT=self.PG_PORT_TEST,
            PG_DB=self.PG_DB_TEST,
        )

    _REDIS_URL: str = "redis://{REDIS_HOST}:{REDIS_PORT}"

    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: str = os.getenv("REDIS_PORT")

    @property
    def REDIS_URL(self) -> str:
        return self._REDIS_URL.format(REDIS_HOST=self.REDIS_HOST, REDIS_PORT=self.REDIS_PORT)

    RESET_PSW_TOKEN_EXPIRES: int = int(os.getenv("RESET_PSW_TOKEN_EXPIRES"))

    EMAIL_HOST: str = os.getenv("EMAIL_SMTP_SERVER")
    EMAIL_PORT: int = int(os.getenv("EMAIL_PORT"))
    EMAIL_USERNAME: str = os.getenv("EMAIL_USERNAME")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")
    EMAIL_SENDER: str = os.getenv("EMAIL_SENDER")
    TEST_EMAIL_RECEIVER: str = os.getenv("TEST_EMAIL_RECEIVER")


env = Env()


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
