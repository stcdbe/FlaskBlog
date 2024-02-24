from flask import redirect, url_for, render_template, Blueprint, Response
from werkzeug.exceptions import Unauthorized, Forbidden, NotFound, InternalServerError

error_router = Blueprint(name='errors',
                         import_name=__name__,
                         static_folder='static',
                         template_folder='templates')


@error_router.app_errorhandler(code=401)
def catch_401_error(error: Unauthorized) -> Response:
    return redirect(url_for('auth.login'))


@error_router.app_errorhandler(code=403)
def catch_403_error(error: Forbidden) -> Response:
    return redirect(url_for('auth.login'))


@error_router.app_errorhandler(code=404)
def catch_404_error(error: NotFound) -> str:
    return render_template('error/not_found.html')


@error_router.app_errorhandler(code=500)
def catch_500_error(error: InternalServerError) -> str:
    return render_template('error/server_trouble.html')
