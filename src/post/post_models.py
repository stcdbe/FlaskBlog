from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import TimedBaseModel
from src.post.post_enums import PostGroup, PostCategory

if TYPE_CHECKING:
    from src.user.user_models import User


class Post(TimedBaseModel):
    __tablename__ = 'post'
    title: Mapped[str] = mapped_column(index=True, unique=True)
    slug: Mapped[str] = mapped_column(index=True, unique=True)
    intro: Mapped[str | None]
    text: Mapped[str] = mapped_column(Text)
    picture: Mapped[str]
    group: Mapped[PostGroup]
    category: Mapped[PostCategory]
    creator_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))
    creator: Mapped['User'] = relationship(back_populates='posts')
    comments: Mapped[list['Comment']] = relationship(cascade='all, delete-orphan',
                                                     order_by='Comment.created_at.desc()')


class Comment(TimedBaseModel):
    __tablename__ = 'comment'
    text: Mapped[str]
    post_id: Mapped[UUID] = mapped_column(ForeignKey('post.id'))
    post: Mapped['Post'] = relationship(back_populates='comments')
    creator_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))
    creator: Mapped['User'] = relationship(back_populates='comments')
