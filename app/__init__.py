from flask import Flask
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_redmail import RedMail
from flask_admin import Admin
from flask_migrate import Migrate
import click
from werkzeug.security import generate_password_hash

from app.config import ProductionConfig, DevelopmentConfig


login_manager = LoginManager()
mail = RedMail()
jwt = JWTManager()
db = SQLAlchemy()
migrate = Migrate()

app = Flask(__name__)

# app.config.from_object(obj=DevelopmentConfig)
app.config.from_object(obj=ProductionConfig)

login_manager.init_app(app=app)
login_manager.session_protection = "strong"
mail.init_app(app=app)
jwt.init_app(app=app)
db.init_app(app=app)
migrate.init_app(app=app, db=db)

from app.user import verifyviews, profileviews, resetpswviews, authors
from app.posts import mainpage, postsviews, searchviews
from app.database import dbmodels, dbfuncs
from app.admin import adminviews
from app.errors import errorviews


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file(filename='images/favicon.ico')


admin = Admin(app=app,
              name='FlaskBlogAdmin',
              template_mode='bootstrap4',
              index_view=adminviews.DashboardView(name='Statistics'))
admin.add_view(adminviews.UserView(model=dbmodels.User,
                                   session=db.session,
                                   name='Users'))
admin.add_view(adminviews.NewsView(model=dbmodels.News,
                                   session=db.session,
                                   name='News'))
admin.add_view(adminviews.ArticleView(model=dbmodels.Article,
                                      session=db.session,
                                      name='Articles'))
admin.add_view(adminviews.ArticleCommentView(model=dbmodels.ArticleComment,
                                             session=db.session,
                                             name='Article Comments'))


@app.cli.command('create-superuser', help='Create a superuser before start.')
@click.argument('username')
@click.argument('password')
def createsuperuser(username: str, password: str) -> None:
    if len(username) < 6 or len(username) > 100:
        print('Username must be between 6 and 100 characters long')
        return
    elif len(password) < 6 or len(password) > 100:
        print('Password must be between 6 and 100 characters long')
        return
    hashedpsw = generate_password_hash(password=password,
                                       method='pbkdf2:sha512')
    superuserdata = {'username': username,
                     'email': 'admin@admin.admin',
                     'password': hashedpsw,
                     'status': 'Admin'}
    dbfuncs.addnewuser(userdata=superuserdata)
    print('Superuser has been created')
