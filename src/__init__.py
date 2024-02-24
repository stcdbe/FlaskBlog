from flask import Flask, Response
from flask.helpers import get_flashed_messages
from flask_admin import Admin
from flask_injector import FlaskInjector
from injector import Injector, singleton
from flask_sqlalchemy import SQLAlchemy

from src.admin.admin_views import DashboardView, UserView, PostView, CommentView
from src.auth.auth_views import auth_router
from src.celery import celery_init_app
from src.dependencies import AppModule
from src.error.error_views import error_router
from src.post.main_views import main_page_router
from src.post.post_models import Post, Comment
from src.post.post_views import post_router
from src.user.user_models import User
from src.user.user_views import user_router


def create_app(config_object: object | str) -> Flask:
    Flask.url_for.__annotations__ = {}
    flask_app = Flask(import_name=__name__)

    flask_app.config.from_object(obj=config_object)

    celery_init_app(app=flask_app)

    with flask_app.app_context():
        app_injector = Injector(modules=[AppModule(app=flask_app)])
        db = app_injector.get(interface=SQLAlchemy, scope=singleton)

    admin = Admin(app=flask_app,
                  name='FlaskBlog Admin Dashboard',
                  template_mode='bootstrap4',
                  index_view=DashboardView(name='Statistics'))
    admin.add_view(UserView(model=User, session=db.session, name='Users'))
    admin.add_view(PostView(model=Post, session=db.session, name='Posts'))
    admin.add_view(CommentView(model=Comment, session=db.session, name='Comments'))

    flask_app.register_blueprint(auth_router)
    flask_app.register_blueprint(user_router)
    flask_app.register_blueprint(main_page_router)
    flask_app.register_blueprint(post_router)
    flask_app.register_blueprint(error_router)

    @flask_app.get('/favicon.ico')
    def favicon() -> Response:
        return flask_app.send_static_file(filename='img/favicon.ico')

    FlaskInjector(app=flask_app, injector=app_injector)

    flask_app.jinja_env.globals.update({'url_for': flask_app.url_for, 'get_flashed_messages': get_flashed_messages})

    return flask_app
