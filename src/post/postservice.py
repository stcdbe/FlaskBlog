from typing import Any

from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from src import db
from src.post.postenums import PostGroup, PostCategory
from src.post.postmodels import Post, Comment


def count_posts_db() -> int:
    stmt = select(func.count('*')).select_from(Post)
    return (db.session.execute(stmt)).scalar()


def count_comments_db() -> int:
    stmt = select(func.count('*')).select_from(Comment)
    return (db.session.execute(stmt)).scalar()


def get_post_db(**kwargs: Any) -> Post | None:
    stmt = select(Post).filter_by(**kwargs)
    try:
        return (db.session.execute(stmt)).scalars().first()
    except InvalidRequestError:
        db.session.rollback()


def get_some_posts_db(size: int, **kwargs: Any) -> list[Post]:
    stmt = (select(Post)
            .filter_by(**kwargs)
            .order_by(Post.created_at.desc()))
    return list((db.session.execute(stmt)).scalars().fetchmany(size=size))


def get_posts_pgn(per_page: int,
                  page: int,
                  group: PostGroup,
                  category: PostCategory | None = None,
                  search_query: str | None = None) -> Pagination:
    stmt = (select(Post)
            .where(Post.group == group)
            .order_by(Post.created_at.desc()))
    if category:
        stmt = stmt.where(Post.category == category)
    if search_query:
        stmt = stmt.where(Post.title.contains(search_query))
    return db.paginate(select=stmt, page=page, per_page=per_page)


def create_post_db(post_data: dict[str, Any]) -> Post | None:
    new_post = Post()

    for key, val in post_data.items():
        if hasattr(new_post, key):
            setattr(new_post, key, val)

    try:
        db.session.add(new_post)
        db.session.commit()
        return new_post
    except IntegrityError:
        db.session.rollback()


def upd_post_db(post: Post, upd_data: dict[str, Any]) -> Post | None:
    for key, val in upd_data.items():
        if hasattr(post, key):
            setattr(post, key, val)

    try:
        db.session.commit()
        db.session.refresh(post)
        return post
    except IntegrityError:
        db.session.rollback()


def del_post_db(post: Post) -> None:
    db.session.delete(post)
    db.session.commit()


def create_com_db(post: Post, com_data: dict[str, Any]) -> None:
    new_com = Comment()

    for key, val in com_data.items():
        if hasattr(new_com, key):
            setattr(new_com, key, val)

    post.comments.append(new_com)
    db.session.commit()


def get_com_by_text_db(**kwargs: Any) -> Comment | None:
    stmt = select(Comment).filter_by(**kwargs)
    return db.session.execute(stmt).scalars().first()
