import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, Update


logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        user = event.from_user
        
        if event.text and event.text.startswith('/'):
            logger.info(f"User {user.id} (@{user.username}) executed: {event.text}")
        elif event.text:
            preview = event.text[:50] + "..." if len(event.text) > 50 else event.text
            logger.info(f"User {user.id} (@{user.username}) sent: {preview}")
        
        return await handler(event, data)
