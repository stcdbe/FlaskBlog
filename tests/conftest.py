from collections.abc import Generator
from io import BufferedReader
from pathlib import Path
from typing import Any

import pytest
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner
from flask_sqlalchemy import SQLAlchemy

from src.config import BASE_DIR, TestSettings
from src.main import create_app
from tests.sqlalchemy import create_tables, drop_tables, insert_test_data
from tests.utils import AuthActions


@pytest.fixture(scope="session")
def app() -> Flask:
    return create_app(config_object=TestSettings)


@pytest.fixture(scope="session")
def db(app: Flask) -> Generator[SQLAlchemy, Any, None]:
    sqla_db = app.extensions["sqlalchemy"]
    with app.app_context():
        drop_tables(db=sqla_db)
        create_tables(db=sqla_db)
        insert_test_data(db=sqla_db)
    yield sqla_db
    with app.app_context():
        drop_tables(db=sqla_db)


@pytest.fixture(scope="session")
def client(app: Flask) -> Generator[FlaskClient, Any, None]:
    with app.test_client() as cli:
        yield cli


@pytest.fixture(scope="session")
def cli_runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()


@pytest.fixture(scope="session")
def auth(client: FlaskClient) -> AuthActions:
    return AuthActions(client=client)


@pytest.fixture()
def picture() -> Generator[BufferedReader, Any, None]:
    abs_test_pic_path = BASE_DIR / "tests" / "resources" / "test.jpeg"
    with Path.open(abs_test_pic_path, "rb") as file:
        yield file
