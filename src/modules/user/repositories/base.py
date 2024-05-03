from abc import ABC, abstractmethod
from typing import Any

from src.modules.user.models.entities import User


class AbstractUserRepository(ABC):
    @abstractmethod
    def count(self) -> int: ...

    @abstractmethod
    def get_pgn(
        self,
        page: int,
        per_page: int,
        order_by: str | None = None,
        reverse: bool = False,
        **kwargs: Any,
    ): ...

    @abstractmethod
    def get_one(self, **kwargs: Any) -> User | None: ...

    @abstractmethod
    def create_one(self, user: User) -> User: ...

    @abstractmethod
    def update_one(self, user: User) -> User: ...
