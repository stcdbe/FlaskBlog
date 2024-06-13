from datetime import timedelta
from typing import Any
from uuid import UUID

from flask import render_template, request, url_for
from flask_jwt_extended import create_access_token, decode_token
from flask_login import login_user, logout_user
from injector import inject
from jwt import DecodeError, ExpiredSignatureError, InvalidTokenError

from src.config.enviroment import env
from src.core.utils.email.smtp import SMTPEmailSender
from src.modules.auth.exceptions import InvalidJWTError
from src.modules.auth.utils.hasher.base import AbstractHasher
from src.modules.user.exceptions import InvalidEmailError, InvalidUsernameOrEmailError
from src.modules.user.models.entities import User
from src.modules.user.repositories.base import AbstractUserRepository


class AuthService:
    _repository: AbstractUserRepository
    _email_sender: SMTPEmailSender
    _hasher: AbstractHasher

    @inject
    def __init__(
        self,
        repository: AbstractUserRepository,
        email_sender: SMTPEmailSender,
        hasher: AbstractHasher,
    ) -> None:
        self._repository = repository
        self._email_sender = email_sender
        self._hasher = hasher

    def registrate(self, data: dict[str, Any]) -> User:
        data["password"] = self._hasher.get_psw_hash(psw=data["password"])

        user = User()

        for key, val in data.items():
            if hasattr(user, key):
                setattr(user, key, val)

        user = self._repository.create_one(user=user)
        login_user(user=user, remember=data["remember"])
        return user

    def login(self, data: dict[str, Any]) -> User:
        exc = InvalidUsernameOrEmailError("Invalid username or email.")
        user = self._repository.get_one(username_or_email=data["username_or_email"])

        if not user:
            raise exc

        if not self._hasher.verify_psw(psw_to_check=data["password"], hashed_psw=user.password):
            raise exc

        login_user(user=user, remember=data["remember"])
        return user

    def logout(self) -> None:
        logout_user()

    def forgot_psw(self, email: str) -> None:
        user = self._repository.get_one(email=email)

        if not user:
            msg = "Invalid email address."
            raise InvalidEmailError(msg)

        exp_delta = timedelta(minutes=env.RESET_PSW_TOKEN_EXPIRES)
        token = create_access_token(identity=str(user.id), expires_delta=exp_delta)
        url = request.host_url[:-1] + url_for("auth.reset_password", token=token)

        email_body = render_template("email/reset_psw_email.html", user=user, url=url)
        self._email_sender.send_email.delay(
            email_subject="(Flask Blog) Reset your password",
            email_receivers=[user.email],
            email_body=email_body,
        )

    def validate_token(self, token: str) -> User:
        exp_exc = InvalidJWTError("Expired token.")
        inv_exc = InvalidJWTError("Invalid token.")
        try:
            user_id = UUID(decode_token(encoded_token=token)["sub"])

        except ExpiredSignatureError as exc:
            raise exp_exc from exc

        except (DecodeError, InvalidTokenError, KeyError, ValueError) as exc:
            raise inv_exc from exc

        user = self._repository.get_one(id=user_id)

        if not user:
            raise inv_exc

        return user

    def reset_psw(self, user: User, new_password: str) -> None:
        user.password = self._hasher.get_psw_hash(psw=new_password)
        user = self._repository.update_one(user=user)
        email_body = render_template(
            "email/info_psw_email.html",
            user=user,
            url=request.host_url[:-1] + url_for("auth.forgot_password"),
        )
        self._email_sender.send_email.delay(
            email_subject="(Flask Blog) Your password was reset",
            email_receivers=[user.email],
            email_body=email_body,
        )
