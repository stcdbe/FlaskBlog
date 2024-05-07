from io import BufferedReader

from flask import Flask
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

from src.modules.comment.models.entities import Comment
from src.modules.post.models.entities import Post
from src.modules.post.models.enums import PostCategory, PostGroup
from tests.utils import AuthActions


def test_show_posts(client: FlaskClient) -> None:
    res_get = client.get("/posts")
    assert res_get.status_code == 200
    assert res_get.request.path == "/posts"


def test_create_post(
    client: FlaskClient,
    auth: AuthActions,
    app: Flask,
    db: SQLAlchemy,
    picture: BufferedReader,
) -> None:
    auth.login()

    res_get = client.get("/posts/create")
    assert res_get.status_code == 200
    assert res_get.request.path == "/posts/create"

    data = {
        "title": "new_test_title",
        "group": PostGroup.articles,
        "category": PostCategory.development,
        "intro": "new_test_intro",
        "text": "new_test_long_text",
        "picture": picture,
    }
    res_post = client.post("/posts/create", data=data, follow_redirects=True)
    assert res_post.status_code == 200
    assert len(res_post.history) == 1
    assert res_post.request.path == "/posts"
    data.pop("picture")
    with app.app_context():
        stmt = select(Post).where(Post.title == data["title"])
        post = db.session.execute(stmt).scalars().one()
    for key, val in data.items():
        assert post.__getattribute__(key) == val


def test_show_post_detail(
    app: Flask,
    client: FlaskClient,
    auth: AuthActions,
    db: SQLAlchemy,
) -> None:
    auth.login()

    with app.app_context():
        stmt = select(Post).where(Post.title == "test_title")
        post = db.session.execute(stmt).scalars().one()

    res_get = client.get(f"/posts/{post.slug}")
    assert res_get.status_code == 200
    assert res_get.request.path == f"/posts/{post.slug}"

    com_data = {"text": "test_comment_text"}
    res_post = client.post(f"/posts/{post.slug}", data=com_data)
    assert res_post.status_code == 200
    assert res_post.request.path == f"/posts/{post.slug}"
    with app.app_context():
        stmt = select(Comment).where(Comment.text == com_data["text"])
        comment = db.session.execute(stmt).scalars().one()
    assert comment.post_id == post.id


def test_update_post(
    client: FlaskClient,
    auth: AuthActions,
    app: Flask,
    db: SQLAlchemy,
    picture: BufferedReader,
) -> None:
    auth.login()

    with app.app_context():
        stmt = select(Post).where(Post.title == "test_title")
        post = db.session.execute(stmt).scalars().one()

    res_get = client.get(f"/posts/{post.slug}/update")
    assert res_get.status_code == 200
    assert res_get.request.path == f"/posts/{post.slug}/update"

    data = {
        "title": "upd_test_title",
        "category": PostCategory.administration,
        "intro": "upd_test_intro",
        "text": "upd_test_long_text",
        "picture": picture,
    }
    res_post = client.post(f"/posts/{post.slug}/update", data=data, follow_redirects=True)
    assert res_post.status_code == 200
    assert len(res_post.history) == 1
    assert res_post.request.path == "/posts"
    with app.app_context():
        stmt = select(Post).where(Post.title == data["title"])
        post = db.session.execute(stmt).scalars().one()
    assert post.intro == data["intro"]
    assert post.text == data["text"]
    assert post.category == data["category"]


def test_delete_post(
    client: FlaskClient,
    auth: AuthActions,
    app: Flask,
    db: SQLAlchemy,
) -> None:
    auth.login()

    with app.app_context():
        stmt = select(Post).where(Post.title == "upd_test_title")
        post = db.session.execute(stmt).scalars().one()

    res_post = client.post(f"/posts/{post.slug}/delete", follow_redirects=True)
    assert res_post.status_code == 200
    assert len(res_post.history) == 1
    assert res_post.request.path == "/posts"
    with app.app_context():
        stmt = select(Post).where(Post.title == "upd_test_title")
        deleted_post = db.session.execute(stmt).scalars().first()
    assert deleted_post is None


def test_search(client: FlaskClient) -> None:
    res_get = client.get("/posts/search")
    assert res_get.status_code == 200
    assert res_get.request.path == "/posts/search"
