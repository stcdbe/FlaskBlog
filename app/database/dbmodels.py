from datetime import datetime
from uuid import uuid4

from sqlalchemy import ForeignKey, UUID, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from flask_login import UserMixin

from app import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    # id: Mapped[int] = mapped_column(db.Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    date: Mapped[datetime] = mapped_column(server_default=func.now(), default=datetime.utcnow)
    picture: Mapped[str] = mapped_column(default='default.jpg')
    status: Mapped[str] = mapped_column(default='Default')
    name: Mapped[str | None]
    position: Mapped[str | None]
    company: Mapped[str | None]
    location: Mapped[str | None]
    website: Mapped[str | None]
    github: Mapped[str | None]
    twitter: Mapped[str | None]
    articles: Mapped[list['Article']] = relationship(back_populates='user', cascade='all, delete-orphan')
    comments: Mapped[list['ArticleComment']] = relationship(back_populates='user', cascade='all, delete-orphan')
    news: Mapped[list['News']] = relationship(back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return self.id


class News(db.Model):
    __tablename__ = 'news'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    # id: Mapped[int] = mapped_column(db.Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    text: Mapped[str] = mapped_column(Text)
    picture: Mapped[str]
    username: Mapped[str] = mapped_column(ForeignKey('user.username'))
    user: Mapped[list['User']] = relationship(back_populates='news')
    category: Mapped[str]
    date: Mapped[datetime] = mapped_column(server_default=func.now(), default=datetime.utcnow)

    def __repr__(self) -> str:
        return self.id


class Article(db.Model):
    __tablename__ = 'article'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    # id: Mapped[int] = mapped_column(db.Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    intro: Mapped[str | None] = mapped_column(Text, nullable=True)
    text: Mapped[str] = mapped_column(Text)
    picture: Mapped[str]
    username: Mapped[str] = mapped_column(ForeignKey('user.username'))
    user: Mapped[list['User']] = relationship(back_populates='articles')
    comments: Mapped[list['ArticleComment']] = relationship(cascade='all, delete-orphan')
    category: Mapped[str]
    date: Mapped[datetime] = mapped_column(server_default=func.now(), default=datetime.utcnow)

    def __repr__(self):
        return self.id


class ArticleComment(db.Model):
    __tablename__ = 'comment'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    # id: Mapped[int] = mapped_column(db.Integer, primary_key=True, index=True)
    articleid: Mapped[str] = mapped_column(ForeignKey('article.id'))
    article: Mapped[list['Article']] = relationship(back_populates='comments')
    username: Mapped[str] = mapped_column(ForeignKey('user.username'))
    user: Mapped[list['User']] = relationship(back_populates='comments')
    text: Mapped[str]
    date: Mapped[datetime] = mapped_column(server_default=func.now(), default=datetime.utcnow)

    def __repr__(self):
        return self.id
