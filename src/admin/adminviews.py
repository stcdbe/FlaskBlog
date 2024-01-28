from typing import Any

from flask import abort, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from jinja2.runtime import Context
from markupsafe import Markup
from wtforms.validators import DataRequired, Length, Optional

from src.user.usermodels import User
from src.post.postmodels import Post
from src.user.userenums import UserStatus
from src.post.postservice import count_posts_db, count_comments_db
from src.user.userservice import count_users_db
from src.utils import delete_picture


class DashboardView(AdminIndexView):
    def is_accessible(self) -> bool | None:
        if (not current_user.is_anonymous) and (current_user.status == UserStatus.Admin):
            return current_user.is_authenticated

    def inaccessible_callback(self, name: str, **kwargs: Any) -> None:
        abort(404)

    @expose('/')
    def index(self) -> str:
        users_count = count_users_db()
        posts_count = count_posts_db()
        comments_count = count_comments_db()
        return self.render('admin/index.html',
                           users_count=users_count,
                           posts_count=posts_count,
                           comments_count=comments_count)


class UserView(ModelView):
    def is_accessible(self) -> bool | None:
        if (not current_user.is_anonymous) and (current_user.status == UserStatus.Admin):
            return current_user.is_authenticated

    def inaccessible_callback(self, name: str, **kwargs: Any) -> None:
        abort(404)

    def show_picture(self, context: Context, model: User, name: str) -> Markup:
        url = url_for('static', filename='img/profileimages/' + model.picture)
        return Markup(f'<img src="{url}" width="100">')

    page_size = 12
    can_create = False
    can_delete = False
    can_edit = False
    edit_modal = True
    column_descriptions = {'status': '''Default - can leave comments;
                                        Author - can create, update posts;
                                        Admin - access to the admin panel;'''}
    can_view_details = True
    details_modal = True
    column_display_pk = True
    column_list = ('id', 'username', 'email', 'status', 'join_date', 'picture',)
    column_details_exclude_list = ['password', ]
    column_sortable_list = ('username', 'email', 'join_date',)
    column_searchable_list = ['id', 'username', 'email', 'join_date', ]
    column_formatters = {'picture': show_picture}


class PostView(ModelView):
    def is_accessible(self) -> bool | None:
        if (not current_user.is_anonymous) and (current_user.status == UserStatus.Admin):
            return current_user.is_authenticated

    def inaccessible_callback(self, name: str, **kwargs: Any) -> None:
        abort(404)

    def show_picture(self, context: Context, model: Post, name: str) -> Markup:
        url = url_for('static', filename='img/postimages/' + model.picture)
        return Markup(f'<img src="{url}" width="200">')

    def after_model_delete(self, model: Post) -> None:
        delete_picture(pic_name=model.picture, img_catalog='postimages')

    page_size = 12
    can_create = False
    edit_modal = True
    form_columns = ('intro', 'text', 'group', 'category',)
    form_args = {'intro': {'label': 'Intro',
                           'validators': [Optional(), Length(max=300)]},
                 'text': {'label': 'Text',
                          'validators': [DataRequired(), Length(min=10, max=5000)]}}
    can_view_details = True
    details_modal = True
    column_display_pk = True
    column_list = ('id', 'title', 'group', 'category', 'user_id', 'created_at', 'picture',)
    column_sortable_list = ('title', 'created_at',)
    column_searchable_list = ['id', 'title', 'category', 'user_id', 'created_at', ]
    column_formatters = {'picture': show_picture}


class CommentView(ModelView):
    def is_accessible(self) -> bool | None:
        if (not current_user.is_anonymous) and (current_user.status == UserStatus.Admin):
            return current_user.is_authenticated

    def inaccessible_callback(self, name: str, **kwargs: Any) -> None:
        abort(404)

    page_size = 12
    can_create = False
    can_edit = False
    can_view_details = True
    details_modal = True
    column_display_pk = True
    column_list = ('id', 'post_id', 'user_id', 'text', 'created_at',)
    column_details_list = ['id', 'post_id', 'user_id', 'text', 'created_at', ]
    column_sortable_list = ('created_at',)
    column_searchable_list = ['id', 'post_id', 'user_id', 'created_at', ]
