from typing import Any

from flask import redirect, url_for, render_template, Blueprint
from werkzeug.exceptions import Unauthorized, Forbidden, NotFound, InternalServerError

error_router = Blueprint('errors',
                         __name__,
                         static_folder='static',
                         template_folder='templates')


@error_router.app_errorhandler(401)
def catch_401_error(error: Unauthorized) -> Any:
    return redirect(url_for('auth.login'))


@error_router.app_errorhandler(403)
def catch_403_error(error: Forbidden) -> Any:
    return redirect(url_for('auth.login'))


@error_router.app_errorhandler(404)
def catch_404_error(error: NotFound) -> Any:
    return render_template('error/notfound.html')


@error_router.app_errorhandler(500)
def catch_500_error(error: InternalServerError) -> Any:
    return render_template('error/servertrouble.html')
