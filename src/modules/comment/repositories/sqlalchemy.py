from sqlalchemy import func, select

from src.core.repositories.sqlalchemy import SQLAlchemyRepository
from src.modules.comment.models.entities import Comment
from src.modules.comment.repositories.base import AbstractCommentRepository


class SQLAlchemyCommentRepository(AbstractCommentRepository, SQLAlchemyRepository):
    def count(self) -> int:
        stmt = select(func.count()).select_from(Comment)
        res = self._db.session.execute(stmt)
        return res.scalars().one()

    def create_one(self, com: Comment) -> Comment:
        self._db.session.add(com)
        self._db.session.commit()
        self._db.session.refresh(com)
        return com
