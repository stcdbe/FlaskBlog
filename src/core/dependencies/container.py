from uuid import UUID

from flask import Flask
from flask_admin import Admin
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from injector import Binder, Module, provider, singleton

from src.core.models.sqlalchemy import BaseModel
from src.core.services.email.smtp import SMTPEmailSender
from src.core.services.picture.manager import PictureManager
from src.modules.admin.views.comment import CommentView
from src.modules.admin.views.dashboard import DashboardView
from src.modules.admin.views.post import PostView
from src.modules.admin.views.user import UserView
from src.modules.auth.services.services import AuthService
from src.modules.comment.models.entities import Comment
from src.modules.comment.repositories.sqlalchemy import SQLAlchemyCommentRepository
from src.modules.comment.services.services import CommentService
from src.modules.post.models.entities import Post
from src.modules.post.repositories.sqlalchemy import SQLAlchemyPostRepository
from src.modules.post.services.services import PostService
from src.modules.user.models.entities import User
from src.modules.user.repositories.sqlalchemy import SQLAlchemyUserRepository
from src.modules.user.services.services import UserService


class AppModule(Module):
    def __init__(self, app: Flask) -> None:
        self.app = app

    def configure(self, binder: Binder) -> None:
        # Flask plugins
        db = self.configure_db()
        self.configure_migrations(db=db)
        self.configure_jwt()
        self.configure_login(db=db)
        self.configure_admin(db=db)

        # SQLAlchemy db instance
        binder.bind(interface=SQLAlchemy, to=db, scope=singleton)

        # Repositories
        binder.bind(interface=SQLAlchemyUserRepository, scope=singleton)
        binder.bind(interface=SQLAlchemyPostRepository, scope=singleton)
        binder.bind(interface=SQLAlchemyCommentRepository, scope=singleton)

        # Services
        binder.bind(interface=UserService)
        binder.bind(interface=AuthService)
        binder.bind(interface=PostService)
        binder.bind(interface=CommentService)

        # Utils
        binder.bind(interface=SMTPEmailSender)
        binder.bind(interface=PictureManager)

    @provider
    @singleton
    def configure_db(self) -> SQLAlchemy:
        return SQLAlchemy(
            app=self.app,
            model_class=BaseModel,
            session_options={"expire_on_commit": False},
        )

    @provider
    @singleton
    def configure_migrations(self, db: SQLAlchemy) -> Migrate:
        return Migrate(app=self.app, db=db)

    @provider
    @singleton
    def configure_jwt(self) -> JWTManager:
        return JWTManager(app=self.app)

    @provider
    @singleton
    def configure_login(self, db: SQLAlchemy) -> LoginManager:
        login_manager = LoginManager(app=self.app)
        login_manager.session_protection = "strong"

        @login_manager.user_loader
        def load_user(user_id: str) -> User | None:
            return db.session.get(User, UUID(user_id))

        return login_manager

    @provider
    @singleton
    def configure_admin(self, db: SQLAlchemy) -> Admin:
        admin = Admin(
            app=self.app,
            name="FlaskBlog Admin Dashboard",
            template_mode="bootstrap4",
            index_view=DashboardView(name="Statistics"),
        )
        admin.add_view(UserView(model=User, session=db.session, name="Users"))
        admin.add_view(PostView(model=Post, session=db.session, name="Posts"))
        admin.add_view(CommentView(model=Comment, session=db.session, name="Comments"))
        return admin
