from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Message, MessageRole
from dao import MessageDao


class MessageService:
    
    @classmethod
    async def add_message(
        cls,
        session: AsyncSession,
        user_id: int,
        role: MessageRole,
        content: str
    ) -> Message:
        message_data = {
            "user_id": user_id,
            "role": role,
            "content": content
        }
        return await MessageDao.create(session, message_data)
    
    @classmethod
    async def get_user_messages(
        cls,
        session: AsyncSession,
        user_id: int,
        limit: int = 20
    ) -> list[Message]:
        return await MessageDao.get_user_messages(session, user_id, limit)
    
    @classmethod
    async def get_messages_count(
        cls,
        session: AsyncSession,
        user_id: int
    ) -> int:
        messages = await MessageDao.find_all_by_filters(session, {"user_id": user_id})
        return len(messages)
    
    @classmethod
    async def clear_user_messages(
        cls,
        session: AsyncSession,
        user_id: int
    ) -> int:
        count = await MessageDao.delete_user_messages(session, user_id)
        await session.commit()
        return count
    
    @classmethod
    async def get_context_for_ai(
        cls,
        session: AsyncSession,
        user_id: int,
        limit: int = 20
    ) -> list[dict]:
        messages = await cls.get_user_messages(session, user_id, limit)
        return [msg.to_dict() for msg in messages]
    
    @classmethod
    async def save_conversation_turn(
        cls,
        session: AsyncSession,
        user_id: int,
        user_message: str,
        assistant_response: str
    ) -> tuple[Message, Message]:
        user_msg = await cls.add_message(
            session, user_id, MessageRole.USER, user_message
        )
        assistant_msg = await cls.add_message(
            session, user_id, MessageRole.ASSISTANT, assistant_response
        )
        return user_msg, assistant_msg
