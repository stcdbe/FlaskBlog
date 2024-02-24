from flask import render_template, Blueprint
from injector import inject

from src.post.post_enums import PostGroup, PostCategory
from src.post.post_models import Post
from src.post.post_services import PostService

main_page_router = Blueprint(name='main',
                             import_name=__name__,
                             static_folder='static',
                             template_folder='templates')


@main_page_router.get(rule='/')
@inject
def show_main_page(post_service: PostService) -> str:
    articles = post_service.get_list(limit=7,
                                     order_by=Post.created_at.desc(),
                                     group=PostGroup.articles)
    news = post_service.get_list(limit=10,
                                 order_by=Post.created_at.desc(),
                                 group=PostGroup.news)
    return render_template('post/main_page.html',
                           articles=articles,
                           news=news,
                           categories=PostCategory)
