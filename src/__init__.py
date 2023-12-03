from typing import Any

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_redmail import RedMail
from flask_admin import Admin
from flask_migrate import Migrate
import click
from werkzeug.security import generate_password_hash

from src.config import ProductionConfig, DevelopmentConfig


login_manager = LoginManager()
mail = RedMail()
jwt = JWTManager()
db = SQLAlchemy()
migrate = Migrate()

app = Flask(__name__)

# app.config.from_object(obj=DevelopmentConfig)
app.config.from_object(obj=ProductionConfig)

login_manager.init_app(app=app)
login_manager.session_protection = 'strong'
mail.init_app(app=app)
jwt.init_app(app=app)
db.init_app(app=app)
migrate.init_app(app=app, db=db)


@app.get('/favicon.ico')
def favicon() -> Any:
    return app.send_static_file(filename='images/favicon.ico')


from src.user import userviews, userservice
from src.auth import authviews, resetpswviews
from src.post import postviews
from src.database import dbmodels, enums
from src.admin import adminviews
from src.errors import errorviews


admin = Admin(app=app,
              name='FlaskBlogAdmin',
              template_mode='bootstrap4',
              index_view=adminviews.DashboardView(name='Statistics'))
admin.add_view(adminviews.UserView(model=dbmodels.User,
                                   session=db.session,
                                   name='Users'))
admin.add_view(adminviews.PostView(model=dbmodels.Post,
                                   session=db.session,
                                   name='Posts'))
admin.add_view(adminviews.CommentView(model=dbmodels.Comment,
                                      session=db.session,
                                      name='Comments'))


@app.cli.command('create-superuser', help='Create a superuser before start.')
@click.argument('username')
@click.argument('email')
@click.argument('password')
def create_superuser(username: str, email: str, password: str) -> None:
    for val in [username, email, password]:
        if len(val) not in range(6, 101):
            print(f'Length of {val} not in range 6-100 characters')
            return
    hashed_psw = generate_password_hash(password=password, method='pbkdf2:sha512')
    superuser_data = {'username': username,
                      'email': email,
                      'password': hashed_psw,
                      'status': enums.UserStatus.Admin}
    if superuser := userservice.create_user_db(user_data=superuser_data):
        print(f'Superuser {superuser.username} has been created.')
        return
    print('Failed to create superuser.')
