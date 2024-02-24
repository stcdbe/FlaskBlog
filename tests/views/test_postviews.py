from typing import BinaryIO

from flask import Flask
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

from src.post.post_enums import PostCategory, PostGroup
from src.post.post_models import Post, Comment
from tests.testutils import TestAuthActions


def test_show_posts(client: FlaskClient) -> None:
    res_get = client.get('/posts')
    assert res_get.status_code == 200
    assert res_get.request.path == '/posts'


def test_create_post(client: FlaskClient,
                     auth: TestAuthActions,
                     app: Flask,
                     db: SQLAlchemy,
                     test_picture: BinaryIO) -> None:
    auth.login()

    res_get = client.get('/posts/create')
    assert res_get.status_code == 200
    assert res_get.request.path == '/posts/create'

    post_data = {'title': 'new_test_title',
                 'group': PostGroup.articles,
                 'category': PostCategory.development,
                 'intro': 'new_test_intro',
                 'text': 'new_test_long_text',
                 'picture': test_picture}
    res_post = client.post('/posts/create',
                           data=post_data,
                           follow_redirects=True)
    assert res_post.status_code == 200
    assert len(res_post.history) == 1
    assert res_post.request.path == '/posts'
    post_data.pop('picture')
    with app.app_context():
        stmt = select(Post).where(Post.title == post_data['title'])
        post = db.session.execute(stmt).scalars().one()
    for key, val in post_data.items():
        assert post.__getattribute__(key) == val


def test_show_post_detail(app: Flask,
                          client: FlaskClient,
                          auth: TestAuthActions,
                          db: SQLAlchemy) -> None:
    auth.login()

    with app.app_context():
        stmt = select(Post).where(Post.title == 'test_title')
        post = db.session.execute(stmt).scalars().one()

    res_get = client.get(f'/posts/{post.slug}')
    assert res_get.status_code == 200
    assert res_get.request.path == f'/posts/{post.slug}'

    com_data = {'text': 'test_comment_text'}
    res_post = client.post(f'/posts/{post.slug}', data=com_data)
    assert res_post.status_code == 200
    assert res_post.request.path == f'/posts/{post.slug}'
    with app.app_context():
        stmt = select(Comment).where(Comment.text == com_data['text'])
        comment = db.session.execute(stmt).scalars().one()
    assert comment.post_id == post.id


def test_update_post(client: FlaskClient,
                     auth: TestAuthActions,
                     app: Flask,
                     db: SQLAlchemy,
                     test_picture: BinaryIO) -> None:
    auth.login()

    with app.app_context():
        stmt = select(Post).where(Post.title == 'test_title')
        post = db.session.execute(stmt).scalars().one()

    res_get = client.get(f'/posts/{post.slug}/update')
    assert res_get.status_code == 200
    assert res_get.request.path == f'/posts/{post.slug}/update'

    upd_post_data = {'title': 'upd_test_title',
                     'category': PostCategory.administration,
                     'intro': 'upd_test_intro',
                     'text': 'upd_test_long_text',
                     'picture': test_picture}
    res_post = client.post(f'/posts/{post.slug}/update',
                           data=upd_post_data,
                           follow_redirects=True)
    assert res_post.status_code == 200
    assert len(res_post.history) == 1
    assert res_post.request.path == '/posts'
    with app.app_context():
        stmt = select(Post).where(Post.title == upd_post_data['title'])
        upd_post = db.session.execute(stmt).scalars().one()
    assert upd_post.intro == upd_post_data['intro']
    assert upd_post.text == upd_post_data['text']
    assert upd_post.category == upd_post_data['category']


def test_delete_post(client: FlaskClient,
                     auth: TestAuthActions,
                     app: Flask,
                     db: SQLAlchemy) -> None:
    auth.login()

    with app.app_context():
        stmt = select(Post).where(Post.title == 'upd_test_title')
        post = db.session.execute(stmt).scalars().one()

    res_post = client.post(f'/posts/{post.slug}/delete', follow_redirects=True)
    assert res_post.status_code == 200
    assert len(res_post.history) == 1
    assert res_post.request.path == '/posts'
    with app.app_context():
        stmt = select(Post).where(Post.title == 'upd_test_title')
        deleted_post = db.session.execute(stmt).scalars().first()
    assert deleted_post is None


def test_search(client: FlaskClient) -> None:
    res_get = client.get('/posts/search')
    assert res_get.status_code == 200
    assert res_get.request.path == f'/posts/search'
