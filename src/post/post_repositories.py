from typing import Any

from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import select, func, ColumnElement
from sqlalchemy.exc import IntegrityError

from src.post.post_exceptions import InvalidPostTitleError
from src.post.post_models import Comment, Post
from src.repositories import SQLAlchemyRepository


class PostRepository(SQLAlchemyRepository):
    def count(self) -> int:
        stmt = select(func.count('*')).select_from(Post)
        res = self.db.session.execute(stmt)
        return res.scalar()

    def get_list(self,
                 limit: int,
                 order_by: str | ColumnElement | None = None,
                 **kwargs: Any) -> list[Post]:
        stmt = select(Post).filter_by(**kwargs).limit(limit).order_by(order_by)
        res = self.db.session.execute(stmt)
        return list(res.scalars().all())

    def get_pgn(self,
                per_page: int,
                page: int,
                order_by: str | ColumnElement | None = None,
                query: str | None = None,
                **kwargs: Any) -> Pagination | None:
        stmt = select(Post).filter_by(**kwargs).order_by(order_by)

        if query:
            stmt = stmt.where(Post.title.contains(query))

        return self.db.paginate(select=stmt, page=page, per_page=per_page)

    def get_one(self, **kwargs: Any) -> Post | None:
        stmt = select(Post).filter_by(**kwargs)
        res = self.db.session.execute(stmt)
        return res.scalars().first()

    def create_one(self, new_post: Post) -> Post:
        try:
            self.db.session.add(new_post)
            self.db.session.commit()

        except IntegrityError:
            self.db.session.rollback()
            raise InvalidPostTitleError('Post title must be unique.')

        else:
            self.db.session.refresh(new_post)
            return new_post

    def update_one(self, post: Post) -> Post:
        try:
            self.db.session.commit()

        except IntegrityError:
            self.db.session.rollback()
            raise InvalidPostTitleError('Post title must be unique.')

        else:
            self.db.session.refresh(post)
            return post

    def del_one(self, post: Post) -> None:
        self.db.session.delete(post)
        self.db.session.commit()


class CommentRepository(SQLAlchemyRepository):
    def count(self) -> int:
        stmt = select(func.count('*')).select_from(Comment)
        res = self.db.session.execute(stmt)
        return res.scalar()

    def get_list(self, **kwargs: Any) -> list[Comment]:
        stmt = select(Comment).filter_by(**kwargs)
        res = self.db.session.execute(stmt)
        return list(res.scalars().all())

    def get_one(self, **kwargs: Any) -> Comment | None:
        stmt = select(Comment).filter_by(**kwargs)
        res = self.db.session.execute(stmt)
        return res.scalars().first()

    def create_one(self, new_com: Comment) -> Comment:
        self.db.session.add(new_com)
        self.db.session.commit()
        self.db.session.refresh(new_com)
        return new_com

    def update_one(self, comment: Comment) -> Comment:
        self.db.session.commit()
        self.db.session.refresh(comment)
        return comment
