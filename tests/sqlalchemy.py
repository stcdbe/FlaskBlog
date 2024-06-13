from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from slugify import slugify

from src.config.enviroment import env
from src.modules.auth.utils.hasher.werkzeug import WerkzeugHasher
from src.modules.post.models.entities import Post
from src.modules.post.models.enums import PostCategory, PostGroup
from src.modules.user.models.entities import User
from src.modules.user.models.enums import UserStatus


def create_tables(db: SQLAlchemy) -> None:
    db.create_all()


def drop_tables(db: SQLAlchemy) -> None:
    db.drop_all()


def insert_test_data(db: SQLAlchemy) -> None:
    user_id = uuid4()

    test_user = User(
        id=user_id,
        username="auth_username",
        email=env.TEST_EMAIL_RECEIVER,
        password=WerkzeugHasher().get_psw_hash("Password123"),
        status=UserStatus.admin,
    )

    test_post = Post(
        title="test_title",
        slug=slugify("test_title"),
        intro="test_intro",
        text="text_long_text",
        group=PostGroup.articles,
        category=PostCategory.development,
        picture="pass",
        creator_id=user_id,
    )

    db.session.add_all((test_user, test_post))
    db.session.commit()
