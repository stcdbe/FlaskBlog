from abc import ABC, abstractmethod

from src.modules.comment.models.entities import Comment


class AbstractCommentRepository(ABC):
    @abstractmethod
    def count(self) -> int: ...

    @abstractmethod
    def create_one(self, com: Comment) -> Comment: ...
