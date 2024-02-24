import logging
import os
from typing import Any

from flask import abort
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from injector import inject
from jinja2.runtime import Context
from markupsafe import Markup
from wtforms.validators import DataRequired, Length, Optional

from src.config import BASE_DIR
from src.post.post_models import Post
from src.post.post_services import PostService, CommentService
from src.user.user_enums import UserStatus
from src.user.user_models import User
from src.user.user_services import UserService


class DashboardView(AdminIndexView):
    def is_accessible(self) -> bool | None:
        if (not current_user.is_anonymous) and (current_user.status == UserStatus.admin):
            return current_user.is_authenticated

    def inaccessible_callback(self, name: str, **kwargs: Any) -> None:
        abort(404)

    @expose('/')
    @inject
    def index(self,
              user_service: UserService,
              post_service: PostService,
              comment_service: CommentService) -> str:
        users_count = user_service.count()
        posts_count = post_service.count()
        comments_count = comment_service.count()
        return self.render(template='admin/index.html',
                           users_count=users_count,
                           posts_count=posts_count,
                           comments_count=comments_count)


class UserView(ModelView):
    def is_accessible(self) -> bool | None:
        if (not current_user.is_anonymous) and (current_user.status == UserStatus.admin):
            return current_user.is_authenticated

    def inaccessible_callback(self, name: str, **kwargs: Any) -> None:
        abort(404)

    def show_picture(self, context: Context, model: User, name: str) -> Markup:
        return Markup(f'<img src="{model.picture}" width="100">')

    page_size = 12
    can_create = False
    can_delete = False
    can_edit = False
    edit_modal = True
    column_descriptions = {'status': '''default - can leave comments;
                                        author - can create, update posts;
                                        admin - access to the admin panel'''}
    can_view_details = True
    details_modal = True
    column_display_pk = True
    column_list = ('id', 'username', 'email', 'status', 'created_at', 'picture')
    column_details_exclude_list = ('password',)
    column_sortable_list = ('username', 'email', 'created_at')
    column_searchable_list = ('id', 'username', 'email', 'created_at')
    column_formatters = {'picture': show_picture}


class PostView(ModelView):
    def is_accessible(self) -> bool | None:
        if (not current_user.is_anonymous) and (current_user.status == UserStatus.admin):
            return current_user.is_authenticated

    def inaccessible_callback(self, name: str, **kwargs: Any) -> None:
        abort(404)

    def show_picture(self, context: Context, model: Post, name: str) -> Markup:
        return Markup(f'<img src="{model.picture}" width="200">')

    def after_model_delete(self, model: Post) -> None:
        abs_pic_path = BASE_DIR / model.picture[1:]
        try:
            os.remove(abs_pic_path)
        except FileNotFoundError:
            logging.warning('Attempt to delete a non-existent file: %s', model.picture)

    page_size = 12
    can_create = False
    edit_modal = True
    form_columns = ('intro', 'text', 'group', 'category')
    form_args = {'intro': {'label': 'Intro',
                           'validators': [Optional(), Length(max=300)]},
                 'text': {'label': 'Text',
                          'validators': [DataRequired(), Length(min=10, max=5000)]}}
    can_view_details = True
    details_modal = True
    column_display_pk = True
    column_list = ('id', 'title', 'group', 'category', 'creator_id', 'created_at', 'picture')
    column_sortable_list = ('title', 'created_at')
    column_searchable_list = ('id', 'title', 'category', 'creator_id', 'created_at')
    column_formatters = {'picture': show_picture}


class CommentView(ModelView):
    def is_accessible(self) -> bool | None:
        if (not current_user.is_anonymous) and (current_user.status == UserStatus.admin):
            return current_user.is_authenticated

    def inaccessible_callback(self, name: str, **kwargs: Any) -> None:
        abort(404)

    page_size = 12
    can_create = False
    can_edit = False
    can_view_details = True
    details_modal = True
    column_display_pk = True
    column_list = ('id', 'post_id', 'creator_id', 'text', 'created_at')
    column_details_list = ('id', 'post_id', 'creator_id', 'text', 'created_at')
    column_sortable_list = ('created_at',)
    column_searchable_list = ('id', 'post_id', 'creator_id', 'created_at')
