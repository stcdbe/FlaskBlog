from abc import ABC, abstractmethod
from typing import Any


class AbstractUserRepository(ABC):
    @abstractmethod
    def count(self, *args: Any, **kwargs: Any): ...

    @abstractmethod
    def get_one(self, *args: Any, **kwargs: Any): ...

    @abstractmethod
    def create_one(self, *args: Any, **kwargs: Any): ...

    @abstractmethod
    def update_one(self, *args: Any, **kwargs: Any): ...
