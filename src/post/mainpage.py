from typing import Any

from flask import render_template, Blueprint

from src.database.enums import PostGroup
from src.post.postservice import get_some_posts_db


main_page_router = Blueprint('main',
                             __name__,
                             static_folder='static',
                             template_folder='templates')


@main_page_router.get('/favicon.ico')
def favicon() -> Any:
    return main_page_router.send_static_file(filename='img/favicon.ico')


@main_page_router.get('/')
def show_main_page() -> Any:
    articles = get_some_posts_db(post_group=PostGroup.articles, size=7)
    news = get_some_posts_db(post_group=PostGroup.news, size=10)
    return render_template('post/mainpage.html', articles=articles, news=news)
