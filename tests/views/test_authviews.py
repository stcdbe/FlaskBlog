from datetime import timedelta

from flask import Flask
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token

from src.config import RESET_PSW_TOKEN_EXPIRES
from src.user.userservice import get_user_by_username_db
from tests.testutils import AuthActions


def test_registration(client: FlaskClient,
                      app: Flask,
                      auth: AuthActions) -> None:
    auth.logout()

    res_get = client.get('/auth/registration')
    assert res_get.status_code == 200
    assert res_get.request.path == '/auth/registration'

    user_data = {'username': 'username',
                 'email': 'email@example.com',
                 'password': 'Password123',
                 'repeat_password': 'Password123'}
    res_post = client.post('/auth/registration',
                           data=user_data,
                           follow_redirects=True)
    assert res_post.status_code == 200
    assert len(res_post.history) == 1
    assert res_post.request.path == '/'
    with app.app_context():
        user = get_user_by_username_db(username=user_data['username'])
    assert user
    assert user.username == user_data['username']
    assert user.email == user_data['email']
    assert user.password != user_data['password']


def test_login(client: FlaskClient, auth: AuthActions) -> None:
    auth.logout()

    res_get = client.get('/auth/login')
    assert res_get.status_code == 200
    assert res_get.request.path == '/auth/login'

    auth_data = {'username_or_email': 'email@example.com', 'password': 'Password123'}
    res_post = client.post('/auth/login',
                           data=auth_data,
                           follow_redirects=True)
    assert res_post.status_code == 200
    assert len(res_post.history) == 1
    assert res_post.request.path == '/'


def test_logout(client: FlaskClient, auth: AuthActions) -> None:
    auth.login()

    res_get = client.get('/auth/logout', follow_redirects=True)
    assert res_get.status_code == 200
    assert len(res_get.history) == 1
    assert res_get.request.path == '/'


def test_forgot_password(client: FlaskClient, auth: AuthActions) -> None:
    auth.logout()

    res_get = client.get('/auth/forgot_password')
    assert res_get.status_code == 200
    assert res_get.request.path == '/auth/forgot_password'

    data = {'username_or_email': 'auth_username'}
    res_post = client.post('/auth/forgot_password',
                           data=data,
                           follow_redirects=True)
    assert res_post.status_code == 200
    assert len(res_post.history) == 1
    assert res_post.request.path == '/auth/login'


def test_reset_password(client: FlaskClient,
                        auth: AuthActions,
                        app: Flask) -> None:
    auth.logout()

    with app.app_context():
        user = get_user_by_username_db(username='auth_username')
        token = create_access_token(identity=str(user.id),
                                    expires_delta=timedelta(minutes=RESET_PSW_TOKEN_EXPIRES))

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
