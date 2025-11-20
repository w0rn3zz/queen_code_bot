from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Message, MessageRole
from dao import MessageDao


class MessageService:
    def __init__(self, session: AsyncSession):
        self.message_dao = MessageDao(session)
    
    async def add_message(
        self,
        user_id: int,
        role: MessageRole,
        content: str
    ) -> Message:
        message_data = {
            "user_id": user_id,
            "role": role,
            "content": content
        }
        return await self.message_dao.create(message_data)
    
    async def get_user_messages(
        self,
        user_id: int,
        limit: int = 20
    ) -> list[Message]:
        return await self.message_dao.get_user_messages(user_id, limit)
    
    async def get_messages_count(
        self,
        user_id: int
    ) -> int:
        return await self.message_dao.count_by_user_id(user_id)
    
    async def clear_user_messages(
        self,
        user_id: int
    ) -> int:
        return await self.message_dao.delete_user_messages(user_id)
    
    async def get_context_for_ai(
        self,
        user_id: int,
        limit: int = 20
    ) -> list[dict]:
        messages = await self.get_user_messages(user_id, limit)
        return [msg.to_dict() for msg in messages]
    
    async def save_conversation_turn(
        self,
        user_id: int,
        user_message: str,
        assistant_response: str
    ) -> tuple[Message, Message]:
        user_msg_data = {
            "user_id": user_id,
            "role": MessageRole.USER,
            "content": user_message
        }
        assistant_msg_data = {
            "user_id": user_id,
            "role": MessageRole.ASSISTANT,
            "content": assistant_response
        }
        
        user_msg = await self.message_dao.create(user_msg_data)
        assistant_msg = await self.message_dao.create(assistant_msg_data)
        
        return user_msg, assistant_msg
