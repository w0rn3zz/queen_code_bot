from aiogram.filters import Filter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from services import AdminService


class IsAdminFilter(Filter):
    
    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        admin_service = AdminService(session)
        return await admin_service.is_admin(message.from_user.id)
