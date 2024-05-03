from abc import ABC, abstractmethod
from typing import Any

from src.modules.post.models.entities import Post


class AbstractPostRepository(ABC):
    @abstractmethod
    def count(self) -> int: ...

    @abstractmethod
    def get_list(
        self,
        limit: int,
        order_by: str | None = None,
        reverse: bool = False,
        **kwargs: Any,
    ) -> list[Post]: ...

    @abstractmethod
    def get_pgn(
        self,
        per_page: int,
        page: int,
        order_by: str | None = None,
        reverse: bool = False,
        query: str | None = None,
        **kwargs: Any,
    ): ...

    @abstractmethod
    def get_one(self, **kwargs: Any) -> Post | None: ...

    @abstractmethod
    def create_one(self, post: Post) -> Post: ...

    @abstractmethod
    def update_one(self, post: Post) -> Post: ...

    @abstractmethod
    def del_one(self, post: Post) -> Post: ...
