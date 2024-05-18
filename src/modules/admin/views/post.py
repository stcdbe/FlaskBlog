import logging
from pathlib import Path
from typing import Any

from flask import abort
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from jinja2.runtime import Context
from markupsafe import Markup
from wtforms.validators import DataRequired, Length, Optional

from src.config import env
from src.modules.post.models.entities import Post
from src.modules.user.models.enums import UserStatus


class PostView(ModelView):
    def is_accessible(self) -> bool:
        if current_user.is_anonymous:
            return False
        if current_user.status != UserStatus.admin:
            return False
        return current_user.is_authenticated

    def inaccessible_callback(self, name: str, **kwargs: Any) -> None:
        abort(404)

    def show_picture(self, context: Context, model: Post, name: str) -> Markup:
        return Markup(f'<img src="{model.picture}" width="200">')

    def after_model_delete(self, model: Post) -> None:
        abs_pic_path = env.BASE_DIR / "src" / model.picture[1:]
        try:
            Path.unlink(abs_pic_path)
        except FileNotFoundError:
            logging.warning("Attempt to delete a non-existent file: %s", abs_pic_path)

    page_size = 12
    can_create = False
    edit_modal = True
    form_columns = ("intro", "text", "group", "category")
    form_args = {
        "intro": {
            "label": "Intro",
            "validators": [Optional(), Length(max=300)],
        },
        "text": {
            "label": "Text",
            "validators": [DataRequired(), Length(min=10, max=5000)],
        },
    }
    can_view_details = True
    details_modal = True
    column_display_pk = True
    column_list = ("id", "title", "group", "category", "creator_id", "created_at", "picture")
    column_sortable_list = ("title", "created_at")
    column_searchable_list = ("id", "title", "category", "creator_id", "created_at")
    column_formatters = {"picture": show_picture}
