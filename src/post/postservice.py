from typing import Any

from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError

from src import db
from src.database.dbmodels import Post, Comment
from src.database.enums import PostGroup, PostCategory


def count_all_posts_db() -> int:
    stmt = func.count(Post.id)
    return db.session.execute(stmt).scalar()


def count_all_comments_db() -> int:
    stmt = func.count(Comment.id)
    return db.session.execute(stmt).scalar()


def get_post_by_slug_db(post_slug: str) -> Post | None:
    stmt = select(Post).where(Post.slug == post_slug)
    return (db.session.execute(stmt)).scalars().first()


def get_post_by_title_db(title: str) -> Post | None:
    stmt = select(Post).where(Post.title == title)
    return db.session.execute(stmt).scalars().first()


def get_some_posts_db(post_group: PostGroup, size: int) -> list[Post]:
    stmt = (select(Post)
            .where(Post.group == post_group)
            .order_by(Post.created_at.desc()))
    return list((db.session.execute(stmt)).scalars().fetchmany(size=size))


def get_posts_pgn(per_page: int,
                  page: int,
                  post_group: PostGroup,
                  category: PostCategory | None = None,
                  search_query: str | None = None) -> Pagination:
    stmt = (select(Post)
            .where(Post.group == post_group)
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


def get_com_by_text_db(text: str) -> Comment | None:
    stmt = select(Comment).where(Comment.text == text)
    return db.session.execute(stmt).scalars().first()
