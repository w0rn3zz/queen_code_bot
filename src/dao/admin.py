from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Admin
from .base import BaseDao


class AdminDao(BaseDao[Admin]):
    model = Admin

    async def is_admin(self, tg_id: int) -> bool:
        query = select(Admin).where(Admin.tg_id == tg_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None
    
    async def get_by_tg_id(self, tg_id: int) -> Admin | None:
        query = select(Admin).where(Admin.tg_id == tg_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def add_admin(self, tg_id: int, added_by_tg_id: int) -> Admin:
        admin = await self.create({
            "tg_id": tg_id,
            "added_by_tg_id": added_by_tg_id
        })
        return admin
    
    async def remove_admin(self, tg_id: int) -> bool:
        admin = await self.find_one_by_filters({"tg_id": tg_id})
        if admin:
            await self.session.delete(admin)
            await self.session.flush()
            return True
        return False
    
    async def get_all_admins(self) -> list[Admin]:
        return await self.find_all()
