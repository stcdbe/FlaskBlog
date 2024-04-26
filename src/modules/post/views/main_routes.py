from flask import Blueprint, render_template
from injector import inject

from src.modules.post.models.enums import PostCategory, PostGroup
from src.modules.post.services.services import PostService

main_page_router = Blueprint(
    name="main",
    import_name=__name__,
    static_folder="static",
    template_folder="templates",
)


@main_page_router.get(rule="/")
@inject
def show_main_page(post_service: PostService) -> str:
    articles = post_service.get_list(
        limit=7,
        order_by="created_at",
        reverse=True,
        group=PostGroup.articles,
    )
    news = post_service.get_list(
        limit=10,
        order_by="created_at",
        reverse=True,
        group=PostGroup.news,
    )
    return render_template(
        "post/main_page.html",
        articles=articles,
        news=news,
        categories=PostCategory,
    )
