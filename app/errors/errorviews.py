from flask import redirect, url_for, render_template, Response
from werkzeug.exceptions import Unauthorized, Forbidden, NotFound, InternalServerError

from app import app


@app.errorhandler(401)
def getloginerror(error: Unauthorized) -> Response:
    return redirect(url_for('signin'))


@app.errorhandler(403)
def forbidenerror(error: Forbidden) -> Response:
    return redirect(url_for('signin'))


@app.errorhandler(404)
def notfound(error: NotFound) -> str:
    return render_template('errors/notfounderror.html')


@app.errorhandler(500)
def servertrouble(error: InternalServerError) -> str:
    return render_template('errors/servererror.html')
