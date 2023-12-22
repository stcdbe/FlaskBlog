from typing import Any
from uuid import UUID

from flask_sqlalchemy.pagination import Pagination
from psycopg2 import DataError
from sqlalchemy import select, and_, func
from sqlalchemy.exc import DBAPIError

from src import db
from src.database.dbmodels import Post, Comment
from src.database.enums import PostGroup, PostCategory


def count_all_posts_db() -> int:
    stmt = func.count(Post.id)
    return db.session.execute(stmt).scalar()


def count_all_comments_db() -> int:
    stmt = func.count(Comment.id)
    return db.session.execute(stmt).scalar()


def get_some_posts_db(post_group: PostGroup, size: int) -> list[Post]:
    stmt = (select(Post)
            .where(Post.group == post_group)
            .order_by(Post.created_at.desc()))
    return list((db.session.execute(stmt)).scalars().fetchmany(size=size))


def get_posts_pgn(post_group: PostGroup,
                  per_page: int,
                  page: int = 1,
                  category: PostCategory | None = None) -> Pagination | None:
    if category:
        stmt = (select(Post)
                .where(and_(Post.group == post_group,
                            Post.category == category))
                .order_by(Post.created_at.desc()))
    else:
        stmt = (select(Post)
                .where(Post.group == post_group)
                .order_by(Post.created_at.desc()))
    return db.paginate(select=stmt, page=page, per_page=per_page)


def get_post_db(post_id: UUID) -> Post | None:
    stmt = select(Post).where(Post.id == post_id)
    try:
        return (db.session.execute(stmt)).scalars().first()
    except (DBAPIError, DataError):
        return


def add_post_db(post_data: dict[str, Any]) -> None:
    new_post = Post()
    for key, val in post_data.items():
        setattr(new_post, key, val)
    db.session.add(new_post)
    db.session.commit()


def upd_post_db(post: Post, upd_data: dict[str, Any]) -> None:
    for key, val in upd_data.items():
        setattr(post, key, val)
    db.session.commit()


def del_post_db(post: Post) -> None:
    db.session.delete(post)
    db.session.commit()


def add_com_db(post: Post, com_data: dict[str, Any]) -> None:
    new_com = Comment()
    for key, val in com_data.items():
        setattr(new_com, key, val)
    post.comments.append(new_com)
    db.session.commit()


def search_posts_db(query: str,
                    post_group: PostGroup,
                    page: int,
                    per_page: int) -> Pagination:
    stmt = (select(Post)
            .where(and_(Post.group == post_group,
                        Post.title.contains(query))))
    return db.paginate(select=stmt, page=page, per_page=per_page)
