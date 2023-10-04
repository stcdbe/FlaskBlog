from flask import request, render_template

from app import app
from app.database.dbfuncs import getauthorspgn


@app.route('/authors')
def showauthors() -> str:
    page = request.args.get('page', default=1, type=int)
    pgn = getauthorspgn(pagenum=page)
    return render_template('user/authors.html', pagination=pgn)
