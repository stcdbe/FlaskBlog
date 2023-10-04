from typing import Type

from flask import url_for, Markup, abort, flash
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.view import log, gettext
from flask_login import current_user
from jinja2.runtime import Context
from wtforms.validators import DataRequired, Length

from app import db
from app.utils import deletepicture
from app.database.dbmodels import User, News, Article, ArticleComment


class DashboardView(AdminIndexView):
    def is_accessible(self) -> bool:
        if not current_user.is_anonymous and current_user.status == 'Admin':
            return current_user.is_authenticated

    def inaccessible_callback(self, name: str, **kwargs) -> None:
        abort(404)

    @expose('/')
    def index(self) -> str:
        users = db.session.execute(db.func.count(User.id)).scalar()
        news = db.session.execute(db.func.count(News.id)).scalar()
        articles = db.session.execute(db.func.count(Article.id)).scalar()
        comments = db.session.execute(db.func.count(ArticleComment.id)).scalar()
        return self.render('admin/index.html',
                           users=users,
                           news=news,
                           articles=articles,
                           articlecomments=comments)


class UserView(ModelView):
    def is_accessible(self) -> bool:
        if not current_user.is_anonymous and current_user.status == 'Admin':
            return current_user.is_authenticated

    def inaccessible_callback(self, name: str, **kwargs) -> None:
        abort(404)

    def showpicture(self, context: Context, model: User, name: str) -> Markup:
        url = url_for('static', filename='images/profileimages/' + model.picture)
        return Markup(f'<img src="{url}" width="100">')

    def delete_model(self, model: User) -> bool:
        if model.status == 'Admin':
            flash(gettext(f'Failed to delete record. User {model.username} is admin.'), 'error')
            log.exception('Failed to delete record.')
            return False
        try:
            self.on_model_delete(model)
            deletepicture(picname=model.picture, imgcatalog='profileimages')
            self.session.flush()
            self.session.delete(model)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to delete record. %(error)s', error=str(ex)), 'error')
                log.exception('Failed to delete record.')
            self.session.rollback()
            return False
        else:
            self.after_model_delete(model)
        return True

    page_size = 15
    can_create = False
    edit_modal = True
    column_descriptions = dict(status='Default - can only leave comments,'
                                      ' Author - can create, edit articles and newsposts,'
                                      ' Admin - access to the admin panel ')
    column_editable_list = ['status', ]
    form_columns = ('status',)
    form_choices = dict(status=[('Default', 'Default'),
                                ('Author', 'Author'), ])
    can_view_details = True
    details_modal = True
    column_display_pk = True
    column_list = ('username', 'email', 'picture', 'status', 'date',)
    column_details_exclude_list = ['password', ]
    column_sortable_list = ('username', 'email', 'date',)
    column_searchable_list = ['username', 'email', 'date', ]
    column_formatters = dict(picture=showpicture)


class NewsView(ModelView):
    def is_accessible(self) -> str:
        if not current_user.is_anonymous and current_user.status == 'Admin':
            return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs) -> None:
        abort(404)

    def showpicture(self, context: Context, model: Type[News | Article], name: str) -> Markup:
        url = url_for('static', filename='images/postimages/' + model.picture)
        return Markup(f'<img src="{url}" width="200">')

    def delete_model(self, model: type[News | Article]) -> bool:
        try:
            self.on_model_delete(model)
            deletepicture(picname=model.picture, imgcatalog='postimages')
            self.session.flush()
            self.session.delete(model)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to delete record. %(error)s', error=str(ex)), 'error')
                log.exception('Failed to delete record.')
            self.session.rollback()
            return False
        else:
            self.after_model_delete(model)
        return True

    page_size = 10
    can_create = False
    edit_modal = True
    form_columns = ('title', 'text', 'category',)
    form_args = dict(title=dict(label='Title', validators=[DataRequired(), Length(min=10, max=100)]),
                     text=dict(label='Text', validators=[DataRequired(), Length(min=10, max=500)]))
    form_choices = dict(category=[('Development', 'Development'),
                                  ('Administration', 'Administration'),
                                  ('Design', 'Design'),
                                  ('Management', 'Management'),
                                  ('Marketing', 'Marketing'),
                                  ('Science', 'Science')])
    can_view_details = True
    details_modal = True
    column_display_pk = True
    column_hide_backrefs = False
    column_list = ('title', 'picture', 'category', 'username', 'date', )
    column_sortable_list = ('title', 'username', 'date',)
    column_searchable_list = ['title', 'category', 'username', 'date', ]
    column_formatters = dict(picture=showpicture)


class ArticleView(NewsView):
    form_columns = ('title', 'text', 'intro', 'category',)
    form_args = dict(title=dict(label='Title', validators=[DataRequired(), Length(min=10, max=100)]),
                     intro=dict(label='Intro', validators=[Length(max=300)]),
                     text=dict(label='Text', validators=[DataRequired(), Length(min=10, max=5000)]))
    column_list = ('title', 'intro', 'picture', 'category', 'username', 'date',)
    column_searchable_list = ['title', 'intro', 'category', 'username', 'date', ]


class ArticleCommentView(ModelView):
    def is_accessible(self) -> bool:
        if not current_user.is_anonymous and current_user.status == 'Admin':
            return current_user.is_authenticated

    def inaccessible_callback(self, name: str, **kwargs) -> None:
        abort(404)

    page_size = 20
    can_create = False
    can_edit = False
    can_view_details = True
    details_modal = True
    column_display_pk = True
    column_hide_backrefs = False
    column_list = ('articleid', 'username', 'text', 'date',)
    column_details_list = ['id', 'articleid', 'username', 'text', 'date', ]
    column_sortable_list = ('date',)
    column_searchable_list = ['articleid', 'username', 'date', ]
