from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.sqlalchemy import TimedBaseModel
from src.modules.post.models.enums import PostCategory, PostGroup

if TYPE_CHECKING:
    from src.modules.comment.models.entities import Comment
    from src.modules.user.models.entities import User


class Post(TimedBaseModel):
    __tablename__ = "post"
    title: Mapped[str] = mapped_column(index=True, unique=True)
    slug: Mapped[str] = mapped_column(index=True, unique=True)
    intro: Mapped[str | None]
    text: Mapped[str] = mapped_column(Text)
    picture: Mapped[str]
    group: Mapped[PostGroup]
    category: Mapped[PostCategory]
    creator_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    creator: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(cascade="all, delete-orphan", order_by="Comment.created_at.desc()")
