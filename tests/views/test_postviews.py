from flask import Flask
from flask.testing import FlaskClient

from src.database.enums import PostCategory, PostGroup
from src.post.postservice import get_post_by_title_db, get_com_by_text_db
from tests.testutils import AuthActions, get_test_pic_path


def test_show_posts(client: FlaskClient) -> None:
    params = {'post_group': PostGroup.articles.value,
              'category': None,
              'page': 1}
    res_get = client.get('/posts', query_string=params)
    assert res_get.status_code == 200
    assert res_get.request.path == '/posts'


def test_create_post(client: FlaskClient,
                     auth: AuthActions,
                     app: Flask) -> None:
    params = {'post_group': PostGroup.articles.value}
    auth.login()

    res_get = client.get('/posts/create', query_string=params)
    assert res_get.status_code == 200
    assert res_get.request.path == '/posts/create'

    post_data = {'title': 'test_title',
                 'intro': 'test_intro',
                 'text': 'test_long_text',
                 'category': PostCategory.Development,
                 'picture': (get_test_pic_path(pic_name='test.jpeg')).open('rb'),
                 'submit': True}
    res_post = client.post('/posts/create',
                           query_string=params,
                           data=post_data,
                           follow_redirects=True)
    assert res_post.status_code == 200
    assert len(res_post.history) == 1
    assert res_post.request.path == '/posts'
    post_data.pop('picture')
    post_data.pop('submit')
    with app.app_context():
        post = get_post_by_title_db(title=post_data['title'])
        assert post
        for key, val in post_data.items():
            assert post.__getattribute__(key) == val


def test_show_article_detail(app: Flask,
                             client: FlaskClient,
                             auth: AuthActions) -> None:
    auth.login()

    with app.app_context():
        post = get_post_by_title_db(title='test_title')

    res_get = client.get(f'/posts/{str(post.id)}')
    assert res_get.status_code == 200
    assert res_get.request.path == f'/posts/{str(post.id)}'

    com_data = {'text': 'test_comment_text',
                'submit': True}
    res_post = client.post(f'/posts/{str(post.id)}', data=com_data)
    assert res_post.status_code == 200
    assert res_post.request.path == f'/posts/{str(post.id)}'
    with app.app_context():
        com = get_com_by_text_db(text=com_data['text'])
        assert com


def test_update_post(client: FlaskClient,
                     auth: AuthActions,
                     app: Flask) -> None:
    auth.login()

    with app.app_context():
        post = get_post_by_title_db(title='test_title')

    res_get = client.get(f'/posts/{str(post.id)}/update')
    assert res_get.status_code == 200
    assert res_get.request.path == f'/posts/{str(post.id)}/update'

    upd_post_data = {'title': 'test_title',
                     'intro': 'new_test_intro',
                     'text': 'new_test_long_text',
                     'category': PostCategory.Administration,
                     'picture': (get_test_pic_path(pic_name='test.jpeg')).open('rb'),
                     'submit': True}
    res_post = client.post(f'/posts/{str(post.id)}/update',
                           data=upd_post_data,
                           follow_redirects=True)
    assert res_post.status_code == 200
    assert len(res_post.history) == 1
    assert res_post.request.path == f'/posts/{str(post.id)}'
    with app.app_context():
        upd_post = get_post_by_title_db(title=upd_post_data['title'])
        assert upd_post
        assert upd_post.intro == upd_post_data['intro']
        assert upd_post.text == upd_post_data['text']
        assert upd_post.category == upd_post_data['category']


def test_delete_post(client: FlaskClient,
                     auth: AuthActions,
                     app: Flask) -> None:
    auth.login()

    with app.app_context():
        post = get_post_by_title_db(title='test_title')

    res_post = client.post(f'/posts/{str(post.id)}/delete', follow_redirects=True)
    assert res_post.status_code == 200
    assert len(res_post.history) == 1
    assert res_post.request.path == '/posts'
    with app.app_context():
        deleted_post = get_post_by_title_db(title='test_title')
        assert deleted_post is None


def test_search(client: FlaskClient) -> None:
    params = {'q': 'test_query', 'page': 1}
    res_get = client.get('/posts/search', query_string=params)
    assert res_get.status_code == 200
    assert res_get.request.path == f'/posts/search'
