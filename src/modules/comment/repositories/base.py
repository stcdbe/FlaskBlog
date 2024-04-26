from abc import ABC, abstractmethod
from typing import Any


class AbstractCommentRepository(ABC):
    @abstractmethod
    def count(self, *args: Any, **kwargs: Any): ...

    @abstractmethod
    def create_one(self, *args: Any, **kwargs: Any): ...
