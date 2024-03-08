from typing import Any

from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import ColumnElement, select, func, or_
from sqlalchemy.exc import IntegrityError

from src.repositories import SQLAlchemyRepository
from src.user.user_exceptions import InvalidUsernameOrEmailError
from src.user.user_models import User


class UserRepository(SQLAlchemyRepository):
    def count(self) -> int:
        stmt = select(func.count('*')).select_from(User)
        res = self.db.session.execute(stmt)
        return res.scalar()

    def get_list(self, **kwargs: Any) -> list[User]:
        stmt = select(User).filter_by(**kwargs)
        res = self.db.session.execute(stmt)
        return list(res.scalars().all())

    def get_pgn(self,
                page: int,
                per_page: int,
                order_by: str | ColumnElement | None = None,
                **kwargs: Any) -> Pagination:
        stmt = select(User).filter_by(**kwargs).order_by(order_by)
        return self.db.paginate(select=stmt, page=page, per_page=per_page)

    def get_one(self, username_or_email: str | None = None, **kwargs: Any) -> User:
        stmt = select(User).filter_by(**kwargs)

        if username_or_email is not None:
            stmt = stmt.where(or_(User.username == username_or_email, User.email == username_or_email))

        res = self.db.session.execute(stmt)
        return res.scalars().first()

    def create_one(self, new_user: User) -> User:
        try:
            self.db.session.add(new_user)
            self.db.session.commit()

        except IntegrityError:
            self.db.session.rollback()
            raise InvalidUsernameOrEmailError('An account with such username or email already exists.')

        else:
            self.db.session.refresh(new_user)
            return new_user

    def update_one(self, user: User) -> User:
        try:
            self.db.session.commit()

        except IntegrityError:
            self.db.session.rollback()
            raise InvalidUsernameOrEmailError('An account with such username or email already exists.')

        else:
            self.db.session.refresh(user)
            return user
