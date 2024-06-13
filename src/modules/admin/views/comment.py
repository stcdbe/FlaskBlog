from http import HTTPStatus
from typing import Any

from flask import abort
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from src.modules.user.models.enums import UserStatus


class CommentView(ModelView):
    def is_accessible(self) -> bool:
        if current_user.is_anonymous:
            return False
        if current_user.status != UserStatus.admin:
            return False
        return current_user.is_authenticated

    def inaccessible_callback(self, name: str, **kwargs: Any) -> None:
        abort(code=HTTPStatus.NOT_FOUND)

    page_size = 12
    can_create = False
    can_edit = False
    can_view_details = True
    details_modal = True
    column_display_pk = True
    column_list = ("id", "post_id", "creator_id", "text", "created_at")
    column_details_list = ("id", "post_id", "creator_id", "text", "created_at")
    column_sortable_list = ("created_at",)
    column_searchable_list = ("id", "post_id", "creator_id", "created_at")
