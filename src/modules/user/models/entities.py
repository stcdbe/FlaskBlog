from typing import TYPE_CHECKING

from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.sqlalchemy import TimedBaseModel
from src.modules.user.models.enums import UserStatus

if TYPE_CHECKING:
    from src.modules.comment.models.entities import Comment
    from src.modules.post.models.entities import Post


class User(TimedBaseModel, UserMixin):
    __tablename__ = "user"
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    picture: Mapped[str] = mapped_column(
        server_default="/static/img/userimg/default.jpg", default="/static/img/userimg/default.jpg"
    )
    status: Mapped[UserStatus] = mapped_column(server_default=UserStatus.default, default=UserStatus.default)
    fullname: Mapped[str | None]
    job_title: Mapped[str | None]
    company: Mapped[str | None]
    location: Mapped[str | None]
    website: Mapped[str | None]
    github: Mapped[str | None]
    twitter: Mapped[str | None]
    posts: Mapped[list["Post"]] = relationship(back_populates="creator", cascade="all, delete-orphan")
    comments: Mapped[list["Comment"]] = relationship(back_populates="creator", cascade="all, delete-orphan")
