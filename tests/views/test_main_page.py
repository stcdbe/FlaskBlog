from http import HTTPStatus

from flask.testing import FlaskClient


def test_favicon(client: FlaskClient) -> None:
    res_get = client.get("/favicon.ico")
    assert res_get.status_code == HTTPStatus.OK
    assert res_get.request.path == "/favicon.ico"


def test_show_main_page(client: FlaskClient) -> None:
    res_get = client.get("/")
    assert res_get.status_code == HTTPStatus.OK
    assert res_get.request.path == "/"
