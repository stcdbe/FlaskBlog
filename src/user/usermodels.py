from datetime import datetime
from typing import TYPE_CHECKING

from flask_login import UserMixin
from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src import BaseModel, Post, Comment
from src.user.userenums import UserStatus
if TYPE_CHECKING:
    from src.post.postmodels import Post, Comment


class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    join_date: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                default=datetime.utcnow)
    picture: Mapped[str] = mapped_column(server_default='default.jpg', default='default.jpg')
    status: Mapped[UserStatus] = mapped_column(server_default=UserStatus.Default, default=UserStatus.Default)
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
