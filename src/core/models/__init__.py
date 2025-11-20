from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from core.config import settings


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=settings.db.naming_convention)
    __abstract__ = True


from .mixins import IntPkMixin, TimestampMixin
from .enums import MessageRole
from .user import User
from .message import Message

__all__ = [
    "Base",
    "IntPkMixin",
    "TimestampMixin",
    "User",
    "Message",
    "MessageRole",
]
