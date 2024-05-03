from typing import Any
from uuid import UUID

from injector import inject

from src.modules.comment.models.entities import Comment
from src.modules.comment.repositories.base import AbstractCommentRepository


class CommentService:
    _repository: AbstractCommentRepository

    @inject
    def __init__(self, repository: AbstractCommentRepository) -> None:
        self._repository = repository

    def count(self) -> int:
        return self._repository.count()

    def create_one(self, data: dict[str, Any], post_id: UUID, creator_id: UUID) -> Comment:
        com = Comment(post_id=post_id, creator_id=creator_id)

        for key, val in data.items():
            if hasattr(com, key):
                setattr(com, key, val)

        return self._repository.create_one(com=com)
