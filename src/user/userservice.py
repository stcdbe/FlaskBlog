from typing import Any
from uuid import UUID

from flask_sqlalchemy.pagination import Pagination
from psycopg2 import DataError
from sqlalchemy import select, or_
from sqlalchemy.exc import DBAPIError, IntegrityError

from src import db
from src.database.dbmodels import User
from src.database.enums import UserStatus
from src.utils import delete_picture


def get_user_db(user_id: UUID | str) -> User | None:
    stmt = select(User).where(User.id == user_id)
    try:
        return (db.session.execute(stmt)).scalars().first()
    except (DBAPIError, DataError):
        return


def get_user_by_username_db(username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    return (db.session.execute(stmt)).scalars().first()


def get_user_by_username_or_email_db(username_or_email: str) -> User | None:
    stmt = select(User).where(or_(User.username == username_or_email,
                                  User.email == username_or_email))
    return (db.session.execute(stmt)).scalars().first()


def create_user_db(user_data: dict[str, Any]) -> User | None:
    new_user = User()

    for key, val in user_data.items():
        setattr(new_user, key, val)

    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except IntegrityError:
        db.session.rollback()
        return


def update_user_db(user: User, upd_data: dict[str, Any]) -> User | None:
    if upd_data.get('picture'):
        delete_picture(pic_name=user.picture, img_catalog='profileimages')

    for key, val in upd_data.items():
        setattr(user, key, val)
    db.session.commit()
    db.session.refresh(user)
    return user


def get_users_pgn(user_status: UserStatus, page: int = 1) -> Pagination:
    stmt = (select(User)
            .where(User.status == user_status)
            .order_by(User.username))
    return db.paginate(select=stmt, page=page, per_page=10)
