from abc import ABC, abstractmethod
from typing import NoReturn, Any

from flask_sqlalchemy import SQLAlchemy
from injector import inject


class AbstractRepository(ABC):
    @abstractmethod
    def count(self, *args: Any, **kwargs: Any) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    def get_one(self, *args: Any, **kwargs: Any) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    def get_list(self, *args: Any, **kwargs: Any) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    def create_one(self, *args: Any, **kwargs: Any) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    def update_one(self, *args: Any, **kwargs: Any) -> NoReturn:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository, ABC):
    db: SQLAlchemy

    @inject
    def __init__(self, db: SQLAlchemy) -> None:
        self.db = db
