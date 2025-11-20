from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base
from .mixins import IntPkMixin, TimestampMixin

if TYPE_CHECKING:
    from core.models import Message

class User(Base, IntPkMixin, TimestampMixin):
    __tablename__ = "users"
    
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, tg_id={self.tg_id}, username={self.username})>"
