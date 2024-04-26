from typing import Any

from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import desc, func, select
from sqlalchemy.exc import IntegrityError

from src.core.repositories.sqlalchemy import SQLAlchemyRepository
from src.modules.post.exceptions.exceptions import InvalidPostTitleError
from src.modules.post.models.entities import Post
from src.modules.post.repositories.base import AbstractProjectRepository


class SQLAlchemyPostRepository(AbstractProjectRepository, SQLAlchemyRepository):
    def count(self) -> int:
        stmt = select(func.count()).select_from(Post)
        res = self.db.session.execute(stmt)
        return res.scalars().one()

    def get_list(
        self,
        limit: int,
        order_by: str | None = None,
        reverse: bool = False,
        **kwargs: Any,
    ) -> list[Post]:
        stmt = select(Post).filter_by(**kwargs).limit(limit)

        if order_by:
            if reverse:
                stmt = stmt.order_by(desc(order_by))
            else:
                stmt = stmt.order_by(order_by)

        res = self.db.session.execute(stmt)
        return list(res.scalars().all())

    def get_pgn(
        self,
        per_page: int,
        page: int,
        order_by: str | None = None,
        reverse: bool = False,
        query: str | None = None,
        **kwargs: Any,
    ) -> Pagination:
        stmt = select(Post).filter_by(**kwargs)

        if order_by:
            if reverse:
                stmt = stmt.order_by(desc(order_by))
            else:
                stmt = stmt.order_by(order_by)

        if query:
            stmt = stmt.where(Post.title.contains(query))

        return self.db.paginate(select=stmt, page=page, per_page=per_page)

    def get_one(self, **kwargs: Any) -> Post | None:
        stmt = select(Post).filter_by(**kwargs)
        res = self.db.session.execute(stmt)
        return res.scalars().first()

    def create_one(self, post: Post) -> Post:
        try:
            self.db.session.add(post)
            self.db.session.commit()

        except IntegrityError:
            self.db.session.rollback()
            raise InvalidPostTitleError("Post title must be unique.")

        else:
            self.db.session.refresh(post)
            return post

    def update_one(self, post: Post) -> Post:
        try:
            self.db.session.commit()

        except IntegrityError:
            self.db.session.rollback()
            raise InvalidPostTitleError("Post title must be unique.")

        else:
            self.db.session.refresh(post)
            return post

    def del_one(self, post: Post) -> None:
        self.db.session.delete(post)
        self.db.session.commit()
