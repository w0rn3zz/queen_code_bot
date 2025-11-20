import logging

from sqlalchemy.ext.asyncio import AsyncSession

from ai.gigachat_client import GigaChatClient
from services.message import MessageService
from core.models import MessageRole
from core.config import settings


logger = logging.getLogger(__name__)


class AIService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.message_service = MessageService(session)
        self.giga_client = GigaChatClient()
    
    async def generate_response(
        self,
        user_id: int,
        user_message: str,
    ) -> str:
        try:
            await self.message_service.add_message(
                user_id=user_id,
                role=MessageRole.USER,
                content=user_message
            )
            
            messages = await self._prepare_context(user_id)
            
            ai_response = await self.giga_client.generate_response(
                messages=messages,
                temperature=settings.ai.temperature,
                max_tokens=settings.ai.max_tokens
            )
            
            await self.message_service.add_message(
                user_id=user_id,
                role=MessageRole.ASSISTANT,
                content=ai_response
            )
            
            return ai_response
            
        except Exception as e:
            logger.error(f"AI generation error for user {user_id}: {e}")
            return "Извините, произошла ошибка. Попробуйте позже."
    
    async def _prepare_context(
        self,
        user_id: int,
    ) -> list[dict[str, str]]:
        history = await self.message_service.get_user_messages(
            user_id, 
            settings.ai.context_limit
        )
        messages = [{"role": "system", "content": settings.ai.system_prompt}]
        
        for msg in reversed(history):
            role = "user" if msg.role == MessageRole.USER else "assistant"
            messages.append({
                "role": role,
                "content": msg.content
            })
        
        return messages
    
    async def clear_history(self, user_id: int) -> int:
        return await self.message_service.clear_user_messages(user_id)
