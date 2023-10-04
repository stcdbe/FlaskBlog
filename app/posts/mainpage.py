from flask import render_template

from app import app
from app.database.dbfuncs import getmainposts
from app.database.dbmodels import Article, News


@app.route('/')
@app.route('/main')
def main() -> str:
    articles = getmainposts(tablemodel=Article, size=7)
    news = getmainposts(tablemodel=News, size=10)
    return render_template('posts/main.html', articles=articles, news=news)
