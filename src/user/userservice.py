from typing import Any

from flask_sqlalchemy.pagination import Pagination
from psycopg2 import DataError
from sqlalchemy import select, or_, func
from sqlalchemy.exc import DBAPIError, IntegrityError, InvalidRequestError

from src import db
from src.user.usermodels import User


def count_users_db() -> int:
    stmt = select(func.count('*')).select_from(User)
    return (db.session.execute(stmt)).scalar()


def get_user_db(**kwargs: Any) -> User | None:
    stmt = select(User)

    if 'username_or_email' in kwargs:
        username_or_email = kwargs.pop('username_or_email')
        stmt = (stmt.where(or_(User.username == username_or_email,
                               User.email == username_or_email))
                .filter_by(**kwargs))
    else:
        stmt = stmt.filter_by(**kwargs)

    try:
        return (db.session.execute(stmt)).scalars().first()
    except (DBAPIError, DataError, InvalidRequestError):
        db.session.rollback()


def create_user_db(user_data: dict[str, Any]) -> User | None:
    new_user = User()

    for key, val in user_data.items():
        if hasattr(new_user, key):
            setattr(new_user, key, val)

    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except IntegrityError:
        db.session.rollback()


def update_user_db(user: User, upd_data: dict[str, Any]) -> User | None:
    for key, val in upd_data.items():
        if hasattr(user, key):
            setattr(user, key, val)

    try:
        db.session.commit()
        db.session.refresh(user)
        return user
    except IntegrityError:
        db.session.rollback()


def get_users_pgn(page: int, per_page: int, **kwargs: Any) -> Pagination:
    stmt = (select(User)
            .filter_by(**kwargs)
            .order_by(User.username))
    return db.paginate(select=stmt, page=page, per_page=per_page)
