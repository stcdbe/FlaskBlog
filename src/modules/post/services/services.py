from typing import Any
from uuid import UUID

from flask_sqlalchemy.pagination import Pagination
from injector import inject
from slugify import slugify

from src.core.services.picture.manager import PictureManager
from src.modules.post.models.entities import Post
from src.modules.post.repositories.sqlalchemy import SQLAlchemyPostRepository


class PostService:
    _repository: SQLAlchemyPostRepository

    @inject
    def __init__(self, repository: SQLAlchemyPostRepository, picture_manager: PictureManager) -> None:
        self._repository = repository
        self._picture_manager = picture_manager

    def count(self) -> int:
        return self._repository.count()

    def get_one(self, **kwargs: Any) -> Post | None:
        return self._repository.get_one(**kwargs)

    def get_list(
        self,
        limit: int,
        order_by: str | None = None,
        reverse: bool = False,
        **kwargs: Any,
    ) -> list[Post]:
        return self._repository.get_list(
            limit=limit,
            order_by=order_by,
            reverse=reverse,
            **kwargs,
        )

    def get_pgn(
        self,
        per_page: int,
        page: int,
        order_by: str | None = None,
        reverse: bool = False,
        query: str | None = None,
        **kwargs: Any,
    ) -> Pagination:
        return self._repository.get_pgn(
            per_page=per_page,
            page=page,
            order_by=order_by,
            reverse=reverse,
            query=query,
            **kwargs,
        )

    def create_one(self, data: dict[str, Any], creator_id: UUID) -> Post:
        data["slug"] = slugify(text=data["title"])

        pic_file = data.pop("picture")
        data["picture"] = self._picture_manager.generate_rel_pic_path(
            img_catalog="postimg",
            filename=pic_file.filename,
        )

        new_post = Post(creator_id=creator_id)

        for key, val in data.items():
            if hasattr(new_post, key):
                setattr(new_post, key, val)

        new_post = self._repository.create_one(post=new_post)

        self._picture_manager.create_one(
            pic_file=pic_file,
            rel_pic_path=new_post.picture,
            pic_size=(900, 400),
        )

        return new_post

    def update_one(self, post: Post, data: dict[str, Any]) -> Post:
        data["slug"] = slugify(text=data["title"])

        pic_file = data.pop("picture")
        old_pic_path = post.picture
        if pic_file:
            data["picture"] = self._picture_manager.generate_rel_pic_path(
                img_catalog="postimg", filename=pic_file.filename
            )

        for key, val in data.items():
            if hasattr(post, key):
                setattr(post, key, val)

        post = self._repository.update_one(post=post)

        if pic_file:
            self._picture_manager.create_one(
                pic_file=pic_file,
                rel_pic_path=post.picture,
                pic_size=(900, 400),
            )
            self._picture_manager.delete_one(rel_pic_path=old_pic_path)

        return post

    def del_one(self, post: Post) -> None:
        self._repository.del_one(post=post)
        self._picture_manager.delete_one(rel_pic_path=post.picture)
