from pathlib import Path
from typing import Any, BinaryIO, Generator
from uuid import uuid4

import pytest
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner
from flask_sqlalchemy import SQLAlchemy
from slugify import slugify

from src.config import TEST_EMAIL_RECEIVER, TestSettings
from src.main import create_app
from src.modules.auth.utils.hasher import Hasher
from src.modules.post.models.entities import Post
from src.modules.post.models.enums import PostCategory, PostGroup
from src.modules.user.models.entities import User
from src.modules.user.models.enums import UserStatus
from tests.utils import AuthActions


@pytest.fixture(scope="session")
def app() -> Generator[Flask, Any, None]:
    flask_app = create_app(config_object=TestSettings)
    yield flask_app


@pytest.fixture(scope="session")
def db(app: Flask) -> Generator[SQLAlchemy, Any, None]:
    db = app.extensions["sqlalchemy"]

    user_id = uuid4()

    test_user = User(
        id=user_id,
        username="auth_username",
        email=TEST_EMAIL_RECEIVER,
        password=Hasher.get_psw_hash("Password123"),
        status=UserStatus.admin,
    )

    test_post = Post(
        title="test_title",
        slug=slugify("test_title"),
        intro="test_intro",
        text="text_long_text",
        group=PostGroup.articles,
        category=PostCategory.development,
        picture="pass",
        creator_id=user_id,
    )

    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add_all((test_user, test_post))
        db.session.commit()
    yield db
    with app.app_context():
        db.drop_all()


@pytest.fixture(scope="session")
def client(app: Flask) -> Generator[FlaskClient, Any, None]:
    with app.test_client() as cli:
        yield cli


@pytest.fixture(scope="session")
def cli_runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()


@pytest.fixture(scope="session")
def auth(client: FlaskClient, db) -> AuthActions:
    return AuthActions(client=client)


@pytest.fixture
def test_picture() -> Generator[BinaryIO, Any, None]:
    abs_test_pic_path = Path(__file__).parent / "resources" / "test.jpeg"
    yield abs_test_pic_path.open("rb")
