from pathlib import Path

from flask.testing import FlaskClient
from werkzeug.security import generate_password_hash
from werkzeug.test import TestResponse

from src.config import TEST_EMAIL_RECEIVER
from src.database.enums import UserStatus
from src.user.userservice import create_user_db


class AuthActions:
    def __init__(self, client: FlaskClient) -> None:
        self._client = client

    def create(self, email: str = TEST_EMAIL_RECEIVER, password: str = 'Password123') -> None:
        hashed_psw = generate_password_hash(password=password)
        auth_user_data = {'username': 'auth_username',
                          'email': email,
                          'password': hashed_psw,
                          'status': UserStatus.Admin}
        with self._client.application.app_context():
            create_user_db(user_data=auth_user_data)

    def login(self, email: str = TEST_EMAIL_RECEIVER, password: str = 'Password123') -> TestResponse:
        auth_data = {'username_or_email': email, 'password': password}
        return self._client.post('/auth/login', data=auth_data)

    def logout(self) -> TestResponse:
        return self._client.get('/auth/logout')


def get_test_pic_path(pic_name: str) -> Path:
    return Path(__file__).parent / 'resources' / pic_name
