from uuid import UUID
from typing import Type, Sequence

from flask_sqlalchemy.pagination import Pagination

from app import db
from app.database.dbmodels import User, Article, News, ArticleComment


def getuser(usernameoremail: str) -> User | None:
    user = (db.session.execute(db.select(User)
                               .where(db.or_(User.username == usernameoremail,
                                             User.email == usernameoremail))).scalars().first())
    db.session.commit()
    return user


def getuserbyid(id: UUID) -> User | None:
    user = db.session.execute(db.select(User).where(User.id == id)).scalars().first()
    db.session.commit()
    return user


def addnewuser(data: dict) -> User:
    newuser = User()
    for key, value in data.items():
        setattr(newuser, key, value)
    db.session.add(newuser)
    db.session.commit()
    return newuser


def adduserdata(user: User, data: dict) -> User:
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return user


def getauthorspgn(pagenum: int | None = None) -> Pagination:
    stmt = db.select(User).where(User.status == 'Author').order_by(User.username)
    pgn = db.paginate(select=stmt, page=pagenum, per_page=12)
    db.session.commit()
    return pgn


def getmainposts(tablemodel: type[Article | News], size: int) -> Sequence[Article | News] | None:
    posts = (db.session.execute(db.select(tablemodel).order_by(tablemodel.date.desc()))
             .scalars().fetchmany(size=size))
    db.session.commit()
    return posts


def getpostspgn(tablemodel: Type[Article | News],
                perpage: int,
                page: int | None = None,
                category: str | None = None) -> Pagination:
    if category:
        stmt = (db.select(tablemodel)
                .where(tablemodel.category == category)
                .order_by(tablemodel.date.desc()))
    else:
        stmt = db.select(tablemodel).order_by(tablemodel.date.desc())
    pgn = db.paginate(select=stmt, page=page, per_page=perpage)
    db.session.commit()
    return pgn


def getpostbyid(tablemodel: Type[Article | News], postid: UUID) -> Article | News | None:
    post = db.session.execute(db.select(tablemodel)
                              .where(tablemodel.id == postid)).scalars().first()
    db.session.commit()
    return post


def getcomments(articleid: UUID):
    comments = db.session.execute(db.select(ArticleComment)
                                  .where(ArticleComment.articleid == articleid)
                                  .order_by(ArticleComment.date.desc())).scalars().all()
    db.session.commit()
    return comments


def addpost(data: dict, tablemodel: type[Article | News | ArticleComment]) -> None:
    newpost = tablemodel()
    for key, value in data.items():
        setattr(newpost, key, value)
    db.session.add(newpost)
    db.session.commit()


def updatepost(post: Article | News, data: dict) -> Article | News:
    for key, value in data.items():
        setattr(post, key, value)
    db.session.commit()
    return post


def searcharticle(query: str, page: int | None = None) -> Pagination | None:
    res = (db.select(Article)
           .where(db.or_(Article.title.contains(query), Article.intro.contains(query))))
    pgn = db.paginate(select=res, page=page, per_page=12)
    db.session.commit()
    return pgn
