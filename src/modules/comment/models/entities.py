from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.sqlalchemy import TimedBaseModel

if TYPE_CHECKING:
    from src.modules.post.models.entities import Post
    from src.modules.user.models.entities import User


class Comment(TimedBaseModel):
    __tablename__ = "comment"
    text: Mapped[str]
    post_id: Mapped[UUID] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="comments")
    creator_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    creator: Mapped["User"] = relationship(back_populates="comments")
