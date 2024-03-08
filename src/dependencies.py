from uuid import UUID

from flask import Flask
from flask_admin import Admin
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from injector import Module, Binder, singleton, provider

from src.admin.admin_views import DashboardView, UserView, PostView, CommentView
from src.auth.auth_services import AuthService
from src.models import BaseModel
from src.post.post_models import Post, Comment
from src.post.post_repositories import PostRepository, CommentRepository
from src.post.post_services import PostService, CommentService
from src.services import PictureService, EmailService
from src.user.user_models import User
from src.user.user_repositories import UserRepository
from src.user.user_services import UserService


class AppModule(Module):
    def __init__(self, app: Flask) -> None:
        self.app = app

    def configure(self, binder: Binder) -> None:
        db = self.configure_db()
        self.configure_migrations(db=db)
        self.configure_jwt()
        self.configure_login(db=db)
        self.configure_admin(db=db)

        binder.bind(interface=SQLAlchemy, to=db, scope=singleton)

        user_repo = UserRepository(db=db)
        post_repo = PostRepository(db=db)
        comment_repo = CommentRepository(db=db)

        binder.bind(interface=UserRepository, to=user_repo, scope=singleton)
        binder.bind(interface=PostRepository, to=post_repo, scope=singleton)
        binder.bind(interface=CommentRepository, to=comment_repo, scope=singleton)

        email_service = EmailService()
        picture_service = PictureService()
        user_service = UserService(user_repository=user_repo, picture_service=picture_service)
        auth_service = AuthService(user_repository=user_repo, email_service=email_service)
        post_service = PostService(post_repository=post_repo, picture_service=picture_service)
        comment_service = CommentService(comment_repository=comment_repo)

        binder.bind(interface=PictureService, to=email_service, scope=singleton)
        binder.bind(interface=EmailService, to=picture_service, scope=singleton)
        binder.bind(interface=UserService, to=user_service, scope=singleton)
        binder.bind(interface=AuthService, to=auth_service, scope=singleton)
        binder.bind(interface=PostService, to=post_service, scope=singleton)
        binder.bind(interface=CommentService, to=comment_service, scope=singleton)

    @provider
    @singleton
    def configure_db(self) -> SQLAlchemy:
        return SQLAlchemy(app=self.app,
                          model_class=BaseModel,
                          session_options={'expire_on_commit': False})

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
        login_manager.session_protection = 'strong'

        @login_manager.user_loader
        def load_user(user_id: str) -> User | None:
            return db.session.get(User, UUID(user_id))

        return login_manager

    @provider
    @singleton
    def configure_admin(self, db: SQLAlchemy) -> Admin:
        admin = Admin(app=self.app,
                      name='FlaskBlog Admin Dashboard',
                      template_mode='bootstrap4',
                      index_view=DashboardView(name='Statistics'))
        admin.add_view(UserView(model=User, session=db.session, name='Users'))
        admin.add_view(PostView(model=Post, session=db.session, name='Posts'))
        admin.add_view(CommentView(model=Comment, session=db.session, name='Comments'))
        return admin
