"""
Сервисы для работы с БД
"""

from .user import UserService
from .message import MessageService

__all__ = [
    "UserService",
    "MessageService",
]
