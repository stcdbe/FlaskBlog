from uuid import UUID

from flask import Flask
from flask_admin import Admin
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from src.celery import celery_init_app
from src.database.dbmodels import BaseModel, User, Post, Comment


login_manager = LoginManager()
jwt = JWTManager()
db = SQLAlchemy(model_class=BaseModel)
migrate = Migrate()


def create_app(config_object: object | str) -> Flask:
    app = Flask(__name__)

    app.config.from_object(obj=config_object)

    login_manager.init_app(app=app)
    login_manager.session_protection = 'strong'
    jwt.init_app(app=app)
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    celery_init_app(app=app)

    from src.admin.adminviews import DashboardView, UserView, PostView, CommentView
    from src.user.userviews import user_router
    from src.auth.authviews import auth_router
    from src.post.mainpage import main_page_router
    from src.post.postviews import post_router
    from src.error.errorviews import error_router
    from src.clickcommands import create_superuser
    from src.user.userservice import get_user_db

    @login_manager.user_loader
    def load_user(user_id: str) -> User | None:
        try:
            return get_user_db(user_id=UUID(user_id))
        except ValueError:
            return

    admin = Admin(app=app,
                  name='FlaskBlog Admin Dashboard',
                  template_mode='bootstrap4',
                  index_view=DashboardView(name='Statistics'))
    admin.add_view(UserView(model=User,
                            session=db.session,
                            name='Users'))
    admin.add_view(PostView(model=Post,
                            session=db.session,
                            name='Posts'))
    admin.add_view(CommentView(model=Comment,
                               session=db.session,
                               name='Comments'))

    app.register_blueprint(auth_router)
    app.register_blueprint(user_router)
    app.register_blueprint(main_page_router)
    app.register_blueprint(post_router)
    app.register_blueprint(error_router)
    app.cli.add_command(create_superuser)

    return app
