from flask import Blueprint, redirect, render_template, url_for
from werkzeug.exceptions import Forbidden, InternalServerError, NotFound, Unauthorized
from werkzeug.wrappers.response import Response

error_router = Blueprint(
    name="errors",
    import_name=__name__,
    static_folder="static",
    template_folder="templates",
)


@error_router.app_errorhandler(code=401)
def catch_401_error(_: Unauthorized) -> Response:
    return redirect(url_for("auth.login"))


@error_router.app_errorhandler(code=403)
def catch_403_error(_: Forbidden) -> Response:
    return redirect(url_for("auth.login"))


@error_router.app_errorhandler(code=404)
def catch_404_error(_: NotFound) -> str:
    return render_template("error/not_found.html")


@error_router.app_errorhandler(code=500)
def catch_500_error(_: InternalServerError) -> str:
    return render_template("error/server_trouble.html")
