from datetime import datetime, date
from uuid import uuid4, UUID

from flask_login import UserMixin

from app import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id: db.Mapped[UUID] = db.mapped_column(db.UUID(as_uuid=True), primary_key=True, default=uuid4)
    # id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    username: db.Mapped[str] = db.mapped_column(db.String, unique=True)
    email: db.Mapped[str] = db.mapped_column(db.String, unique=True)
    password: db.Mapped[str]
    date: db.Mapped[date] = db.mapped_column(db.Date, default=date.today())
    picture: db.Mapped[str] = db.mapped_column(db.String, default='default.jpg')
    status: db.Mapped[str] = db.mapped_column(db.String, default='Default')
    name: db.Mapped[str] = db.mapped_column(db.String, nullable=True)
    position: db.Mapped[str] = db.mapped_column(db.String, nullable=True)
    company: db.Mapped[str] = db.mapped_column(db.String, nullable=True)
    location: db.Mapped[str] = db.mapped_column(db.String, nullable=True)
    website: db.Mapped[str] = db.mapped_column(db.String, nullable=True)
    github: db.Mapped[str] = db.mapped_column(db.String, nullable=True)
    twitter: db.Mapped[str] = db.mapped_column(db.String, nullable=True)
    articles: db.Mapped[list['Article']] = db.relationship(back_populates='user', cascade='all, delete-orphan')
    comments: db.Mapped[list['ArticleComment']] = db.relationship(back_populates='user', cascade='all, delete-orphan')
    news: db.Mapped[list['News']] = db.relationship(back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return self.id


class News(db.Model):
    __tablename__ = 'news'
    id: db.Mapped[UUID] = db.mapped_column(db.UUID(as_uuid=True), primary_key=True, default=uuid4)
    # id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: db.Mapped[str]
    text: db.Mapped[str] = db.mapped_column(db.Text)
    picture: db.Mapped[str]
    username: db.Mapped[str] = db.mapped_column(db.ForeignKey('user.username'))
    user: db.Mapped[list['User']] = db.relationship(back_populates='news')
    category: db.Mapped[str]
    date: db.Mapped[datetime] = db.mapped_column(db.DateTime, default=datetime.utcnow().replace(microsecond=0))

    def __repr__(self) -> str:
        return self.id


class Article(db.Model):
    __tablename__ = 'article'
    id: db.Mapped[UUID] = db.mapped_column(db.UUID(as_uuid=True), primary_key=True, default=uuid4)
    # id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: db.Mapped[str]
    intro: db.Mapped[str] = db.mapped_column(db.Text, nullable=True)
    text: db.Mapped[str] = db.mapped_column(db.Text)
    picture: db.Mapped[str]
    username: db.Mapped[str] = db.mapped_column(db.ForeignKey('user.username'))
    user: db.Mapped[list['User']] = db.relationship(back_populates='articles')
    comments: db.Mapped[list['ArticleComment']] = db.relationship(cascade='all, delete-orphan')
    category: db.Mapped[str]
    date: db.Mapped[datetime] = db.mapped_column(db.DateTime, default=datetime.utcnow().replace(microsecond=0))

    def __repr__(self):
        return self.id


class ArticleComment(db.Model):
    __tablename__ = 'comment'
    id: db.Mapped[UUID] = db.mapped_column(db.UUID(as_uuid=True), primary_key=True, default=uuid4)
    # id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    articleid: db.Mapped[str] = db.mapped_column(db.ForeignKey('article.id'))
    article: db.Mapped[list['Article']] = db.relationship(back_populates='comments')
    username: db.Mapped[str] = db.mapped_column(db.ForeignKey('user.username'))
    user: db.Mapped[list['User']] = db.relationship(back_populates='comments')
    text: db.Mapped[str]
    date: db.Mapped[datetime] = db.mapped_column(db.DateTime, default=datetime.utcnow().replace(microsecond=0))

    def __repr__(self):
        return self.id
