from flask import request, render_template

from app import app
from app.database.dbfuncs import searcharticle


@app.route('/search')
def search() -> str:
    query = request.args.get('q', type=str)
    page = request.args.get('page', default=1,  type=int)
    pgn = searcharticle(query=query, page=page)
    return render_template('posts/search.html', query=query, pagination=pgn)
