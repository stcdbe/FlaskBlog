from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from src.config import TEST_EMAIL_RECEIVER


class AuthActions:
    def __init__(self, client: FlaskClient) -> None:
        self._client = client

    def login(self) -> TestResponse:
        data = {"username_or_email": TEST_EMAIL_RECEIVER, "password": "Password123"}
        return self._client.post("/auth/login", data=data)

    def logout(self) -> TestResponse:
        return self._client.get("/auth/logout")
