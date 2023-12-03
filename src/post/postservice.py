from typing import Any
from uuid import UUID

from flask_sqlalchemy.pagination import Pagination
from psycopg2 import DataError
from sqlalchemy import select, and_
from sqlalchemy.exc import DBAPIError

from src import db
from src.database.dbmodels import Post, Comment
from src.database.enums import PostType
from src.utils import delete_picture


def get_some_posts_db(post_type: PostType, size: int) -> list[Post]:
    stmt = (select(Post)
            .where(Post.type == post_type)
            .order_by(Post.created_at.desc()))
    return list((db.session.execute(stmt)).scalars().fetchmany(size=size))


def get_posts_pgn(post_type: PostType,
                  per_page: int,
                  page: int = 1,
                  category: str | None = None) -> Pagination:
    if category:
        stmt = (select(Post)
                .where(and_(Post.type == post_type,
                            Post.category == category))
                .order_by(Post.created_at.desc()))
    else:
        stmt = (select(Post)
                .where(Post.type == post_type)
                .order_by(Post.created_at.desc()))
    return db.paginate(select=stmt, page=page, per_page=per_page)


def get_post_db(post_type: PostType, post_id: UUID | str) -> Post | None:
    stmt = (select(Post)
            .where(and_(Post.type == post_type,
                        Post.id == post_id)))
    try:
        return (db.session.execute(stmt)).scalars().first()
    except (DBAPIError, DataError):
        return


def add_post_db(post_type: PostType, post_data: dict[str, Any]) -> None:
    new_post = Post(type=post_type)
    for key, val in post_data.items():
        setattr(new_post, key, val)
    db.session.add(new_post)
    db.session.commit()


def upd_post_db(post: Post, upd_data: dict[str, Any]) -> None:
    if upd_data.get('picture'):
        delete_picture(pic_name=post.picture, img_catalog='profileimages')

    for key, val in upd_data.items():
        setattr(post, key, val)
    db.session.commit()


def add_com_db(post: Post, com_data: dict[str, Any]) -> None:
    new_com = Comment()
    for key, val in com_data.items():
        setattr(new_com, key, val)
    post.comments.append(new_com)
    db.session.commit()


def search_article_db(query: str, page: int = 1) -> Pagination:
    stmt = (select(Post)
            .where(and_(Post.type == PostType.article_post,
                        Post.title.contains(query))))
    return db.paginate(select=stmt, page=page, per_page=10)
