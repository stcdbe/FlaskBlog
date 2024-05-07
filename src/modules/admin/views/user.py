from typing import Any

from flask import abort
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from jinja2.runtime import Context
from markupsafe import Markup

from src.modules.user.models.entities import User
from src.modules.user.models.enums import UserStatus


class UserView(ModelView):
    def is_accessible(self) -> bool:
        if (not current_user.is_anonymous) and (current_user.status == UserStatus.admin):
            return current_user.is_authenticated
        return False

    def inaccessible_callback(self, name: str, **kwargs: Any) -> None:
        abort(404)

    def show_picture(self, context: Context, model: User, name: str) -> Markup:
        return Markup(f'<img src="{model.picture}" width="100">')

    page_size = 12
    can_create = False
    can_delete = False
    can_edit = False
    edit_modal = True
    column_descriptions = {
        "status": """default - can leave comments;
                     author - can create, update posts;
                     admin - access to the admin panel"""
    }
    can_view_details = True
    details_modal = True
    column_display_pk = True
    column_list = ("id", "username", "email", "status", "created_at", "picture")
    column_details_exclude_list = ("password",)
    column_sortable_list = ("username", "email", "created_at")
    column_searchable_list = ("id", "username", "email", "created_at")
    column_formatters = {"picture": show_picture}
