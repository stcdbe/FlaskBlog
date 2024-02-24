from datetime import timedelta
from typing import Any
from uuid import UUID

from flask import url_for, request, render_template
from flask_jwt_extended import create_access_token, decode_token
from flask_login import login_user, logout_user
from injector import inject
from jwt import InvalidTokenError, ExpiredSignatureError, DecodeError

from src.auth.auth_utils import Hasher
from src.config import RESET_PSW_TOKEN_EXPIRES
from src.services import EmailService
from src.user.user_exceptions import InvalidEmailError, InvalidUsernameOrEmailError, InvalidTokenError
from src.user.user_models import User
from src.user.user_repositories import UserRepository


class AuthService:
    @inject
    def __init__(self, user_repository: UserRepository, email_service: EmailService):
        self.user_repository = user_repository
        self.email_service = email_service

    def registrate(self, user_data: dict[str, Any]) -> User:
        user_data['password'] = Hasher.get_psw_hash(psw=user_data['password'])

        new_user = User()

        for key, val in user_data.items():
            if hasattr(new_user, key):
                setattr(new_user, key, val)

        new_user = self.user_repository.create_one(new_user=new_user)
        login_user(user=new_user, remember=user_data['remember'])
        return new_user

    def login(self, login_data: dict[str, Any]) -> User:
        exc = InvalidUsernameOrEmailError('Invalid username or email.')
        user = self.user_repository.get_one(username_or_email=login_data['username_or_email'])

        if not user:
            raise exc

        if not Hasher.verify_psw(psw_to_check=login_data['password'], hashed_psw=user.password):
            raise exc

        login_user(user=user, remember=login_data['remember'])
        return user

    def logout(self) -> None:
        logout_user()

    def forgot_psw(self, email: str) -> None:
        user = self.user_repository.get_one(email=email)

        if not user:
            raise InvalidEmailError('Invalid email address.')

        exp_delta = timedelta(minutes=RESET_PSW_TOKEN_EXPIRES)
        token = create_access_token(identity=str(user.id), expires_delta=exp_delta)
        url = request.host_url[:-1] + url_for('auth.reset_password', token=token)

        email_body = render_template('email/reset_psw_email.html', **{'user': user, 'url': url})
        self.email_service.send_email.delay(email_subject='(Flask Blog) Reset your password',
                                            email_receivers=[user.email],
                                            email_body=email_body)

    def validate_token(self, token: str) -> User:
        exp_exc = InvalidTokenError('Expired token.')
        inv_exc = InvalidTokenError('Invalid token.')
        try:
            user_id = UUID(decode_token(encoded_token=token)['sub'])

        except ExpiredSignatureError:
            raise exp_exc

        except (DecodeError, InvalidTokenError, KeyError, ValueError):
            raise inv_exc

        user = self.user_repository.get_one(id=user_id)

        if not user:
            raise inv_exc

        return user

    def reset_psw(self, user: User, new_password: str) -> None:
        user.password = Hasher.get_psw_hash(psw=new_password)
        upd_user = self.user_repository.update_one(user=user)

        url = request.host_url[:-1] + url_for('auth.forgot_password')

        email_body = render_template('email/info_psw_email.html', **{'user': upd_user, 'url': url})
        self.email_service.send_email.delay(email_subject='(Flask Blog) Your password was reset',
                                            email_receivers=[upd_user.email],
                                            email_body=email_body)
