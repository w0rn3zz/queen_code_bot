from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Message, MessageRole
from .base import BaseDao


class MessageDao(BaseDao[Message]):
    model = Message
    
    async def get_user_messages(self, user_id: int, limit: int = 20) -> list[Message]:
        query = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .order_by(self.model.created_at.desc())
            .limit(limit)
        )
        res = await self.session.execute(query)
        messages = list(res.scalars().all())
        return list(reversed(messages))
    
    async def count_by_user_id(self, user_id: int) -> int:
        query = select(func.count()).select_from(self.model).where(self.model.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalar()
    
    async def delete_user_messages(self, user_id: int) -> int:
        query = delete(self.model).where(self.model.user_id == user_id)
        result = await self.session.execute(query)
        return result.rowcount
