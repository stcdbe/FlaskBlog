from typing import Any

from flask import abort
from flask_admin import AdminIndexView, expose
from flask_login import current_user
from injector import inject

from src.modules.comment.services.services import CommentService
from src.modules.post.services.services import PostService
from src.modules.user.models.enums import UserStatus
from src.modules.user.services.services import UserService


class DashboardView(AdminIndexView):
    def is_accessible(self) -> bool | None:
        if (not current_user.is_anonymous) and (current_user.status == UserStatus.admin):
            return current_user.is_authenticated

    def inaccessible_callback(self, name: str, **kwargs: Any) -> None:
        abort(404)

    @expose("/")
    @inject
    def index(self, user_service: UserService, post_service: PostService, comment_service: CommentService) -> str:
        users_count = user_service.count()
        posts_count = post_service.count()
        comments_count = comment_service.count()
        return self.render(
            template="admin/index.html",
            users_count=users_count,
            posts_count=posts_count,
            comments_count=comments_count,
        )
