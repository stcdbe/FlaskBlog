from typing import Any
from uuid import UUID

from injector import inject

from src.modules.comment.models.entities import Comment
from src.modules.comment.repositories.sqlalchemy import SQLAlchemyCommentRepository


class CommentService:
    _repository: SQLAlchemyCommentRepository

    @inject
    def __init__(self, repository: SQLAlchemyCommentRepository) -> None:
        self._repository = repository

    def count(self) -> int:
        return self._repository.count()

    def create_one(self, data: dict[str, Any], post_id: UUID, creator_id: UUID) -> Comment:
        com = Comment(post_id=post_id, creator_id=creator_id)

        for key, val in data.items():
            if hasattr(com, key):
                setattr(com, key, val)

        return self._repository.create_one(com=com)
