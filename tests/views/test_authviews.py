from datetime import timedelta

from flask import Flask
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

from src.config import RESET_PSW_TOKEN_EXPIRES
from src.config import TEST_EMAIL_RECEIVER
from src.user.user_enums import UserStatus
from src.user.user_models import User
from tests.testutils import TestAuthActions


def test_registration(client: FlaskClient,
                      app: Flask,
                      auth: TestAuthActions,
                      db: SQLAlchemy) -> None:
    auth.logout()

    res_get = client.get('/auth/registration')
    assert res_get.status_code == 200
    assert res_get.request.path == '/auth/registration'

    user_data = {'username': 'new_test_username',
                 'email': 'new_test_email@example.com',
                 'password': 'Password123',
                 'repeat_password': 'Password123'}
    res_post = client.post('/auth/registration',
                           data=user_data,
                           follow_redirects=True)
    assert res_post.status_code == 200
    assert len(res_post.history) == 1
    assert res_post.request.path == '/'
    with app.app_context():
        stmt = select(User).where(User.username == user_data['username'])
        user = db.session.execute(stmt).scalars().one()
    assert user.username == user_data['username']
    assert user.email == user_data['email']
    assert user.password != user_data['password']
    assert user.status == UserStatus.default


def test_login(client: FlaskClient, auth: TestAuthActions) -> None:
    auth.logout()

    res_get = client.get('/auth/login')
    assert res_get.status_code == 200
    assert res_get.request.path == '/auth/login'

    auth_data = {'username_or_email': TEST_EMAIL_RECEIVER, 'password': 'Password123'}
    res_post = client.post('/auth/login',
                           data=auth_data,
                           follow_redirects=True)
    assert res_post.status_code == 200
    assert len(res_post.history) == 1
    assert res_post.request.path == '/'


def test_logout(client: FlaskClient, auth: TestAuthActions) -> None:
    auth.login()

    res_get = client.get('/auth/logout', follow_redirects=True)
    assert res_get.status_code == 200
    assert len(res_get.history) == 1
    assert res_get.request.path == '/'


def test_forgot_password(client: FlaskClient, auth: TestAuthActions) -> None:
    auth.logout()

    res_get = client.get('/auth/forgot_password')
    assert res_get.status_code == 200
    assert res_get.request.path == '/auth/forgot_password'

    data = {'email': TEST_EMAIL_RECEIVER}
    res_post = client.post('/auth/forgot_password',
                           data=data,
                           follow_redirects=True)
    assert res_post.status_code == 200
    assert len(res_post.history) == 1
    assert res_post.request.path == '/auth/login'


def test_reset_password(client: FlaskClient,
                        auth: TestAuthActions,
                        app: Flask,
                        db: SQLAlchemy) -> None:
    auth.logout()

    exp_delta = timedelta(minutes=RESET_PSW_TOKEN_EXPIRES)
    with app.app_context():
        stmt = select(User).where(User.username == 'auth_username')
        user = db.session.execute(stmt).scalars().one()
        token = create_access_token(identity=str(user.id), expires_delta=exp_delta)

    res_get = client.get('/auth/reset_password/' + token)
    assert res_get.status_code == 200
    assert res_get.request.path == '/auth/reset_password/' + token

    data = {'password': 'Password123', 'repeat_password': 'Password123'}
    res_post = client.post('/auth/reset_password/' + token,
                           data=data,
                           follow_redirects=True)
    assert res_post.status_code == 200
    assert len(res_post.history) == 1
    assert res_post.request.path == '/auth/login'
