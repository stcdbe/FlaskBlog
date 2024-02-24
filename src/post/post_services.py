from typing import Any
from uuid import UUID

from flask_sqlalchemy.pagination import Pagination
from injector import inject
from slugify import slugify
from sqlalchemy import ColumnElement

from src.post.post_models import Post, Comment
from src.post.post_repositories import PostRepository, CommentRepository
from src.services import PictureService


class PostService:
    @inject
    def __init__(self, post_repository: PostRepository, picture_service: PictureService) -> None:
        self.post_repository = post_repository
        self.picture_service = picture_service

    def count(self) -> int:
        return self.post_repository.count()

    def get_one(self, **kwargs: Any) -> Post | None:
        return self.post_repository.get_one(**kwargs)

    def get_list(self,
                 limit: int,
                 order_by: str | ColumnElement | None = None,
                 **kwargs: Any) -> list[Post]:
        return self.post_repository.get_list(limit=limit, order_by=order_by, **kwargs)

    def get_pgn(self,
                per_page: int,
                page: int,
                order_by: str | ColumnElement | None = None,
                query: str | None = None,
                **kwargs: Any) -> Pagination:
        return self.post_repository.get_pgn(per_page=per_page,
                                            page=page,
                                            order_by=order_by,
                                            query=query,
                                            **kwargs)

    def create_one(self, post_data: dict[str, Any], creator_id: UUID) -> Post:
        post_data['slug'] = slugify(text=post_data['title'])

        pic_file = post_data.pop('picture')
        post_data['picture'] = self.picture_service.generate_rel_pic_path(img_catalog='postimg',
                                                                          filename=pic_file.filename)

        new_post = Post(creator_id=creator_id)

        for key, val in post_data.items():
            if hasattr(new_post, key):
                setattr(new_post, key, val)

        new_post = self.post_repository.create_one(new_post=new_post)

        self.picture_service.save_picture(pic_file=pic_file,
                                          rel_pic_path=new_post.picture,
                                          pic_size=(900, 400))

        return new_post

    def update_one(self, post: Post, upd_data: dict[str, Any]) -> Post | None:
        upd_data['slug'] = slugify(text=upd_data['title'])

        pic_file = upd_data.pop('picture')
        old_pic_path = post.picture
        if pic_file:
            upd_data['picture'] = self.picture_service.generate_rel_pic_path(img_catalog='postimg',
                                                                             filename=pic_file.filename)

        for key, val in upd_data.items():
            if hasattr(post, key):
                setattr(post, key, val)

        upd_post = self.post_repository.update_one(post=post)

        if pic_file:
            self.picture_service.save_picture(pic_file=pic_file,
                                              rel_pic_path=upd_post.picture,
                                              pic_size=(900, 400))
            self.picture_service.delete_picture(rel_pic_path=old_pic_path)

        return upd_post

    def del_one(self, post: Post) -> None:
        self.post_repository.del_one(post=post)
        self.picture_service.delete_picture(rel_pic_path=post.picture)


class CommentService:
    @inject
    def __init__(self, comment_repository: CommentRepository) -> None:
        self.comment_repository = comment_repository

    def count(self) -> int:
        return self.comment_repository.count()

    def get_one(self, **kwargs: Any) -> Comment | None:
        return self.comment_repository.get_one(**kwargs)

    def create_one(self,
                   com_data: dict[str, Any],
                   post_id: UUID,
                   creator_id: UUID) -> Comment:
        new_com = Comment(post_id=post_id, creator_id=creator_id)

        for key, val in com_data.items():
            if hasattr(new_com, key):
                setattr(new_com, key, val)

        return self.comment_repository.create_one(new_com=new_com)
