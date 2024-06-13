from http import HTTPStatus

from flask import Blueprint, redirect, render_template, url_for
from werkzeug.exceptions import Forbidden, InternalServerError, NotFound, Unauthorized
from werkzeug.wrappers.response import Response

error_router = Blueprint(
    name="errors",
    import_name=__name__,
    static_folder="static",
    template_folder="templates",
)


@error_router.app_errorhandler(code=HTTPStatus.UNAUTHORIZED)
def catch_401_error(_: Unauthorized) -> tuple[Response, int]:
    return redirect(url_for("auth.login")), HTTPStatus.UNAUTHORIZED


@error_router.app_errorhandler(code=HTTPStatus.FORBIDDEN)
def catch_403_error(_: Forbidden) -> tuple[Response, int]:
    return redirect(url_for("auth.login")), HTTPStatus.FORBIDDEN


@error_router.app_errorhandler(code=HTTPStatus.NOT_FOUND)
def catch_404_error(_: NotFound) -> tuple[str, int]:
    return render_template("error/not_found.html"), HTTPStatus.NOT_FOUND


@error_router.app_errorhandler(code=HTTPStatus.INTERNAL_SERVER_ERROR)
def catch_500_error(_: InternalServerError) -> tuple[str, int]:
    return render_template("error/server_trouble.html"), HTTPStatus.INTERNAL_SERVER_ERROR
