from typing import Generator, Any

import pytest
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner

from src import create_app, db
from src.config import TestSettings
from tests.testutils import AuthActions


@pytest.fixture(scope='session')
def app() -> Generator[Flask, Any, None]:
    app = create_app(config_object=TestSettings)
    with app.app_context():
        db.drop_all()
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture(scope='session')
def client(app: Flask) -> Generator[FlaskClient, Any, None]:
    with app.test_client() as cli:
        yield cli


@pytest.fixture(scope='session')
def cli_runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()


@pytest.fixture(scope='session')
def auth(client: FlaskClient) -> AuthActions:
    au = AuthActions(client)
    au.create()
    return au
