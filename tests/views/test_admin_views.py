from flask.testing import FlaskClient

from tests.utils import AuthActions


def test_admin_dashboard(client: FlaskClient, auth: AuthActions) -> None:
    auth.login()

    res_get = client.get("/admin", follow_redirects=True)
    assert res_get.status_code == 200
    assert res_get.request.path == "/admin/"


def test_users_dashboard(client: FlaskClient, auth: AuthActions) -> None:
    auth.login()

    res_get = client.get("/admin/users")
    assert res_get.status_code == 200
    assert res_get.request.path == "/admin/users"


def test_posts_dashboard(client: FlaskClient, auth: AuthActions) -> None:
    auth.login()

    res_get = client.get("/admin/posts")
    assert res_get.status_code == 200
    assert res_get.request.path == "/admin/posts"


def test_comments_dashboard(client: FlaskClient, auth: AuthActions) -> None:
    auth.login()

    res_get = client.get("/admin/comments")
    assert res_get.status_code == 200
    assert res_get.request.path == "/admin/comments"
