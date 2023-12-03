from typing import Any

from flask import redirect, url_for, render_template
from werkzeug.exceptions import Unauthorized, Forbidden, NotFound, InternalServerError

from src import app


@app.errorhandler(401)
def get_login_error(error: Unauthorized) -> Any:
    return redirect(url_for('signin'))


@app.errorhandler(403)
def get_forbidden_error(error: Forbidden) -> Any:
    return redirect(url_for('signin'))


@app.errorhandler(404)
def get_not_found_error(error: NotFound) -> Any:
    return render_template('errors/notfounderror.html')


@app.errorhandler(500)
def get_server_trouble_error(error: InternalServerError) -> Any:
    return render_template('errors/servererror.html')
