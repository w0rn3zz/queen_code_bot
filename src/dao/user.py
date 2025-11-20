from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from .base import BaseDao


class UserDao(BaseDao[User]):
    model = User
    
    async def find_by_tg_id(self, tg_id: int) -> User | None:
        query = select(self.model).where(self.model.tg_id == tg_id)
        res = await self.session.execute(query)
        return res.scalar_one_or_none()
    
    async def update_by_tg_id(self, tg_id: int, values: dict) -> User | None:
        user = await self.find_by_tg_id(tg_id)
        if not user:
            return None
        
        for key, value in values.items():
            if value is not None:
                setattr(user, key, value)
        
        await self.session.flush()
        await self.session.refresh(user)
        return user
    
    async def upsert(self, tg_id: int, user_data: dict) -> User:
        user = await self.find_by_tg_id(tg_id)
        
        if user:
            for key, value in user_data.items():
                if key != 'tg_id':
                    setattr(user, key, value)
            await self.session.flush()
            await self.session.refresh(user)
        else:
            user = await self.create({"tg_id": tg_id, **user_data})
        
        return user
