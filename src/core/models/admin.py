from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import IntPkMixin, TimestampMixin


class Admin(Base, IntPkMixin, TimestampMixin):
    __tablename__ = "admins"
    
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    added_by_tg_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    
    def __repr__(self) -> str:
        return f"<Admin(id={self.id}, tg_id={self.tg_id})>"
