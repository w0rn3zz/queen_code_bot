from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from .base import BaseDao


class UserDao(BaseDao[User]):
    model = User
    
    @classmethod
    async def find_by_tg_id(cls, session: AsyncSession, tg_id: int) -> User | None:
        query = select(cls.model).where(cls.model.tg_id == tg_id)
        res = await session.execute(query)
        return res.scalar_one_or_none()
