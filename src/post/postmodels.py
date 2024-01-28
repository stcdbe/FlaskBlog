from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src import BaseModel
from src.post.postenums import PostGroup, PostCategory
if TYPE_CHECKING:
    from src.user.usermodels import User


class Post(BaseModel):
    __tablename__ = 'post'
    title: Mapped[str] = mapped_column(index=True, unique=True)
    slug: Mapped[str] = mapped_column(index=True, unique=True)
    intro: Mapped[str | None]
    text: Mapped[str] = mapped_column(Text)
    picture: Mapped[str]
    group: Mapped[PostGroup]
    category: Mapped[PostCategory]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='posts')
    comments: Mapped[list['Comment']] = relationship(cascade='all, delete-orphan',
                                                     order_by='Comment.created_at.desc()')


class Comment(BaseModel):
    __tablename__ = 'comment'
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    post_id: Mapped[UUID] = mapped_column(ForeignKey('post.id'))
    post: Mapped['Post'] = relationship(back_populates='comments')
    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='comments')
