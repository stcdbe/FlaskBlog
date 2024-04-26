from abc import ABC, abstractmethod
from typing import Any


class AbstractProjectRepository(ABC):
    @abstractmethod
    def count(self, *args: Any, **kwargs: Any): ...

    @abstractmethod
    def get_list(self, *args: Any, **kwargs: Any): ...

    @abstractmethod
    def get_one(self, *args: Any, **kwargs: Any): ...

    @abstractmethod
    def create_one(self, *args: Any, **kwargs: Any): ...

    @abstractmethod
    def update_one(self, *args: Any, **kwargs: Any): ...

    @abstractmethod
    def del_one(self, *args: Any, **kwargs: Any): ...
