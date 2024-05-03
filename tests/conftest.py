from pathlib import Path
from typing import Any, BinaryIO, Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner
from flask_sqlalchemy import SQLAlchemy

from src.config import TestSettings
from src.main import create_app
from tests.sqlalchemy import create_tables, drop_tables, insert_test_data
from tests.utils import AuthActions


@pytest.fixture(scope="session")
def app() -> Generator[Flask, Any, None]:
    flask_app = create_app(config_object=TestSettings)
    yield flask_app


@pytest.fixture(scope="session")
def db(app: Flask) -> Generator[SQLAlchemy, Any, None]:
    db = app.extensions["sqlalchemy"]
    with app.app_context():
        drop_tables(db=db)
        create_tables(db=db)
        insert_test_data(db=db)
    yield db
    with app.app_context():
        drop_tables(db=db)


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
