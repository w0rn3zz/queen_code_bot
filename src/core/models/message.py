from typing import TYPE_CHECKING
from sqlalchemy import BigInteger, Text, ForeignKey, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IntPkMixin, TimestampMixin
from .enums import MessageRole

if TYPE_CHECKING:
    from core.models import User

class Message(Base, IntPkMixin, TimestampMixin):
    __tablename__ = "messages"
    
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    
    role: Mapped[MessageRole] = mapped_column(
        Enum(MessageRole, name="message_role"),
    )
    
    content: Mapped[str] = mapped_column(Text)
    
    user: Mapped["User"] = relationship(
        "User",
        back_populates="messages",
        lazy="selectin"
    )
    
    def __repr__(self) -> str:
        content_preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"<Message(id={self.id}, role={self.role.value}, content='{content_preview}')>"
    
    def to_dict(self) -> dict:
        return {
            "role": self.role.value,
            "content": self.content
        }
