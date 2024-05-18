from typing import Any

from flask import Flask, Response, get_flashed_messages, send_from_directory
from flask_injector import FlaskInjector
from injector import Injector

from src.config import env
from src.core.dependencies.container import AppModule
from src.core.workers.celery import celery_init_app
from src.modules.auth.views.routes import auth_router
from src.modules.error.views.routes import error_router
from src.modules.post.views.main_routes import main_page_router
from src.modules.post.views.post_routes import post_router
from src.modules.user.views.routes import user_router


def create_app(config_object: Any) -> Flask:
    Flask.url_for.__annotations__ = {}
    flask_app = Flask(import_name=__name__)

    flask_app.config.from_object(obj=config_object)

    celery_init_app(app=flask_app)

    with flask_app.app_context():
        injector = Injector(modules=(AppModule(app=flask_app),))

    for router in (auth_router, user_router, main_page_router, post_router, error_router):
        flask_app.register_blueprint(blueprint=router)

    @flask_app.get(rule="/favicon.ico")
    def favicon() -> Response:
        return send_from_directory(
            directory=(env.BASE_DIR / "src" / "static" / "img"),
            path="favicon.ico",
            mimetype="image/vnd.microsoft.icon",
        )

    FlaskInjector(app=flask_app, injector=injector)

    flask_app.jinja_env.globals.update(
        {
            "url_for": flask_app.url_for,
            "get_flashed_messages": get_flashed_messages,
        },
    )

    return flask_app
