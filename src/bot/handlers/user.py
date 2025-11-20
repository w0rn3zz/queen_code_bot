from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from services import UserService, MessageService

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession):
    # Пример использования Service через DI сессии
    user_service = UserService(session)
    user = await user_service.get_user(message.from_user.id)
    
    await message.answer(f"Привет, {user.first_name if user else 'незнакомец'}!")