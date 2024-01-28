from flask import Flask
from flask.testing import FlaskClient

from src.user.userservice import get_user_db
from tests.testutils import AuthActions, get_test_pic_path


def test_show_profile(client: FlaskClient, auth: AuthActions) -> None:
    auth.login()

    res_get = client.get('/users/auth_username')
    assert res_get.status_code == 200
    assert res_get.request.path == '/users/auth_username'


def test_update_profile(client: FlaskClient,
                        auth: AuthActions,
                        app: Flask) -> None:
    auth.login()

    res_get = client.get('/users/auth_username/update')
    assert res_get.status_code == 200
    assert res_get.request.path == '/users/auth_username/update'

    upd_user_data = {'picture': (get_test_pic_path(pic_name='test.jpeg')).open('rb'),
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
        upd_user = get_user_db(username='auth_username')
    assert upd_user
    for key, val in upd_user_data.items():
        assert upd_user.__getattribute__(key) == val


def test_show_authors(client: FlaskClient) -> None:
    res_get = client.get('/users/authors')
    assert res_get.status_code == 200
    assert res_get.request.path == '/users/authors'
