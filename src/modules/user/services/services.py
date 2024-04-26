from typing import Any

from flask_sqlalchemy.pagination import Pagination
from injector import inject

from src.core.services.picture.manager import PictureManager
from src.modules.user.models.entities import User
from src.modules.user.repositories.sqlalchemy import SQLAlchemyUserRepository


class UserService:
    _repository: SQLAlchemyUserRepository

    @inject
    def __init__(self, repository: SQLAlchemyUserRepository, picture_manager: PictureManager) -> None:
        self._repository = repository
        self._picture_manager = picture_manager

    def count(self) -> int:
        return self._repository.count()

    def get_one(self, username_or_email: str | None = None, **kwargs: Any) -> User | None:
        return self._repository.get_one(username_or_email=username_or_email, **kwargs)

    def get_pgn(
        self,
        page: int,
        per_page: int,
        order_by: str | None = None,
        reverse: bool = False,
        **kwargs: Any,
    ) -> Pagination:
        return self._repository.get_pgn(
            page=page,
            per_page=per_page,
            order_by=order_by,
            reverse=reverse,
            **kwargs,
        )

    def update_one(self, user: User, data: dict[str, Any]) -> User:
        pic_file = data.pop("picture")
        old_pic_path = user.picture
        if pic_file:
            data["picture"] = self._picture_manager.generate_rel_pic_path(
                img_catalog="userimg",
                filename=pic_file.filename,
            )

        for key, val in data.items():
            if hasattr(user, key):
                setattr(user, key, val)

        upd_user = self._repository.update_one(user=user)

        if pic_file:
            self._picture_manager.create_one(
                pic_file=pic_file,
                rel_pic_path=upd_user.picture,
                pic_size=(250, 250),
            )
            self._picture_manager.delete_one(rel_pic_path=old_pic_path)

        return upd_user
