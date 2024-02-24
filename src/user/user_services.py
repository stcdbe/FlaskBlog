from typing import Any

from flask_sqlalchemy.pagination import Pagination
from injector import inject
from sqlalchemy import ColumnElement

from src.services import PictureService
from src.user.user_models import User
from src.user.user_repositories import UserRepository


class UserService:
    @inject
    def __init__(self, user_repository: UserRepository, picture_service: PictureService) -> None:
        self.user_repository = user_repository
        self.picture_service = picture_service

    def count(self) -> int:
        return self.user_repository.count()

    def get_one(self,
                username_or_email: str | None = None,
                **kwargs: Any) -> User | None:
        return self.user_repository.get_one(username_or_email=username_or_email, **kwargs)

    def get_pgn(self,
                page: int,
                per_page: int,
                order_by: str | ColumnElement | None = None,
                **kwargs: Any) -> Pagination:
        return self.user_repository.get_pgn(page=page,
                                            per_page=per_page,
                                            order_by=order_by,
                                            **kwargs)

    def update_one(self, user: User, upd_data: dict[str, Any]) -> User:
        pic_file = upd_data.pop('picture')
        old_pic_path = user.picture
        if pic_file:
            upd_data['picture'] = self.picture_service.generate_rel_pic_path(img_catalog='userimg',
                                                                             filename=pic_file.filename)

        for key, val in upd_data.items():
            if hasattr(user, key):
                setattr(user, key, val)

        upd_user = self.user_repository.update_one(user=user)

        if pic_file:
            self.picture_service.save_picture(pic_file=pic_file,
                                              rel_pic_path=upd_user.picture,
                                              pic_size=(250, 250))
            self.picture_service.delete_picture(rel_pic_path=old_pic_path)

        return upd_user
