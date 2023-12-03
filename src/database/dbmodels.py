from datetime import datetime
from uuid import uuid4

from sqlalchemy import ForeignKey, UUID, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin

from src import db
from src.database.enums import UserStatus, PostType, PostCategory


class BaseModel(db.Model):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True),
                                     primary_key=True,
                                     default=uuid4,
                                     index=True)

    def __repr__(self) -> str:
        return str(self.id)


class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    join_date: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                default=datetime.utcnow)
    picture: Mapped[str] = mapped_column(server_default='default.jpg', default='default.jpg')
    status: Mapped[UserStatus] = mapped_column(server_default='Default', default='Default')
    fullname: Mapped[str | None]
    job_title: Mapped[str | None]
    company: Mapped[str | None]
    location: Mapped[str | None]
    website: Mapped[str | None]
    github: Mapped[str | None]
    twitter: Mapped[str | None]
    posts: Mapped[list['Post']] = relationship(back_populates='user',
                                               cascade='all, delete-orphan')
    comments: Mapped[list['Comment']] = relationship(back_populates='user',
                                                     cascade='all, delete-orphan')


class Post(BaseModel):
    __tablename__ = 'post'
    title: Mapped[str] = mapped_column(index=True)
    intro: Mapped[str | None]
    text: Mapped[str] = mapped_column(Text)
    picture: Mapped[str]
    type: Mapped[PostType]
    category: Mapped[PostCategory]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='posts')
    comments: Mapped[list['Comment']] = relationship(cascade='all, delete-orphan',
                                                     order_by='Comment.created_at.desc()')


class Comment(BaseModel):
    __tablename__ = 'comment'
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    post_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('post.id'))
    post: Mapped['Post'] = relationship(back_populates='comments')
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='comments')
