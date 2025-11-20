from typing import Callable, Any, Awaitable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Update, User as TgUser

from core.db_helper import DatabaseHelper
from services import UserService


class UpdateUser(BaseMiddleware):
    
    def __init__(self, db_helper: DatabaseHelper) -> None:
        self.db_helper = db_helper

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        tg_user: TgUser | None = data.get("event_from_user")
        
        if tg_user:
            async with self.db_helper.session_factory() as session:
                await UserService.upsert_user(
                    session=session,
                    tg_id=tg_user.id,
                    username=tg_user.username,
                    first_name=tg_user.first_name,
                    last_name=tg_user.last_name,
                )
        
        return await handler(event, data)