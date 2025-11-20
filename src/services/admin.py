from sqlalchemy.ext.asyncio import AsyncSession

from dao import AdminDao
from core.models import Admin
from core.config import settings


class AdminService:
    def __init__(self, session: AsyncSession):
        self.dao = AdminDao(session)
    
    async def is_admin(self, tg_id: int) -> bool:
        if tg_id == settings.bot.admin_id:
            return True
        
        return await self.dao.is_admin(tg_id)
    
    async def add_admin(self, tg_id: int, added_by_tg_id: int) -> Admin:
        return await self.dao.add_admin(tg_id, added_by_tg_id)
    
    async def remove_admin(self, tg_id: int) -> bool:
        return await self.dao.remove_admin(tg_id)
    
    async def get_all_admins(self) -> list[Admin]:
        return await self.dao.get_all_admins()
    
    async def get_by_tg_id(self, tg_id: int) -> Admin | None:
        return await self.dao.get_by_tg_id(tg_id)
