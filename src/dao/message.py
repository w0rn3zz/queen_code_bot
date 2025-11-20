from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Message, MessageRole
from .base import BaseDao


class MessageDao(BaseDao[Message]):
    model = Message
    
    @classmethod
    async def get_user_messages(
        cls,
        session: AsyncSession,
        user_id: int,
        limit: int = 20
    ) -> list[Message]:
        query = (
            select(cls.model)
            .where(cls.model.user_id == user_id)
            .order_by(cls.model.created_at.desc())
            .limit(limit)
        )
        res = await session.execute(query)
        messages = list(res.scalars().all())
        return list(reversed(messages))
    
    @classmethod
    async def delete_user_messages(
        cls,
        session: AsyncSession,
        user_id: int
    ) -> int:
        query = delete(cls.model).where(cls.model.user_id == user_id)
        result = await session.execute(query)
        return result.rowcount
