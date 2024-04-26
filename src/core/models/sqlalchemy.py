from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, index=True)

    def __repr__(self) -> str:
        return f"table: {self.__tablename__}, id: {self.id}"


class TimedBaseModel(BaseModel):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        default=datetime.utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
