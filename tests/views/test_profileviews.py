from typing import BinaryIO

from flask import Flask
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

from src.user.user_models import User
from tests.testutils import TestAuthActions


def test_show_profile(client: FlaskClient, auth: TestAuthActions) -> None:
    auth.login()

    res_get = client.get('/users/auth_username')
    assert res_get.status_code == 200
    assert res_get.request.path == '/users/auth_username'


def test_update_profile(client: FlaskClient,
                        auth: TestAuthActions,
                        app: Flask,
                        db: SQLAlchemy,
                        test_picture: BinaryIO) -> None:
    auth.login()

    res_get = client.get('/users/auth_username/update')
    assert res_get.status_code == 200
    assert res_get.request.path == '/users/auth_username/update'

    upd_user_data = {'picture': test_picture,
                     'fullname': 'test_fullname',
                     'job_title': 'test_position',
                     'location': 'test_location',
                     'company': 'test_company',
                     'website': 'https://example.com/',
                     'github': 'https://example.com/',
                     'twitter': 'https://example.com/'}
    res_post = client.post('/users/auth_username/update',
                           data=upd_user_data,
                           follow_redirects=True)
    assert res_post.status_code == 200
    assert len(res_post.history) == 1
    assert res_post.request.path == '/users/auth_username'
    upd_user_data.pop('picture')
    with app.app_context():
        stmt = select(User).where(User.username == 'auth_username')
        upd_user = db.session.execute(stmt).scalars().one()
    for key, val in upd_user_data.items():
        assert upd_user.__getattribute__(key) == val


def test_show_authors(client: FlaskClient) -> None:
    res_get = client.get('/users/authors')
    assert res_get.status_code == 200
    assert res_get.request.path == '/users/authors'
