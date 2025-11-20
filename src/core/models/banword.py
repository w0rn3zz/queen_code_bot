from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import IntPkMixin, TimestampMixin


class BanWord(Base, IntPkMixin, TimestampMixin):
    __tablename__ = "banwords"
    
    word: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    def __repr__(self) -> str:
        return f"<BanWord(id={self.id}, word={self.word}, is_active={self.is_active})>"
