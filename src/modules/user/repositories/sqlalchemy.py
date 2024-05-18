from typing import Any

from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import desc, func, or_, select
from sqlalchemy.exc import IntegrityError

from src.core.repositories.sqlalchemy import SQLAlchemyRepository
from src.modules.user.exceptions.exceptions import InvalidUsernameOrEmailError
from src.modules.user.models.entities import User
from src.modules.user.repositories.base import AbstractUserRepository


class SQLAlchemyUserRepository(AbstractUserRepository, SQLAlchemyRepository):
    def count(self) -> int:
        stmt = select(func.count()).select_from(User)
        res = self.db.session.execute(stmt)
        return res.scalars().one()

    def get_pgn(
        self,
        page: int,
        per_page: int,
        order_by: str | None = None,
        reverse: bool = False,
        **kwargs: Any,
    ) -> Pagination:
        stmt = select(User).filter_by(**kwargs)

        if order_by:
            if reverse:
                stmt = stmt.order_by(desc(order_by))
            else:
                stmt = stmt.order_by(order_by)

        return self.db.paginate(select=stmt, page=page, per_page=per_page)

    def get_one(self, username_or_email: str | None = None, **kwargs: Any) -> User | None:
        stmt = select(User).filter_by(**kwargs)

        if username_or_email is not None:
            stmt = stmt.where(
                or_(
                    User.username == username_or_email,
                    User.email == username_or_email,
                ),
            )

        res = self.db.session.execute(stmt)
        return res.scalars().first()

    def create_one(self, user: User) -> User:
        try:
            self.db.session.add(user)
            self.db.session.commit()

        except IntegrityError as exc:
            self.db.session.rollback()
            msg = "An account with such username or email already exists."
            raise InvalidUsernameOrEmailError(msg) from exc

        else:
            self.db.session.refresh(user)
            return user

    def update_one(self, user: User) -> User:
        try:
            self.db.session.commit()

        except IntegrityError as exc:
            self.db.session.rollback()
            msg = "An account with such username or email already exists."
            raise InvalidUsernameOrEmailError(msg) from exc

        else:
            self.db.session.refresh(user)
            return user
