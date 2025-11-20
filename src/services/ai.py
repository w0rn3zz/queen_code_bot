import logging

from sqlalchemy.ext.asyncio import AsyncSession

from ai.gigachat_client import GigaChatClient
from services.message import MessageService
from core.models import MessageRole


logger = logging.getLogger(__name__)


class AIService:
    SYSTEM_PROMPT = """Ты — полезный AI-ассистент в Telegram боте. 
Твоя задача — помогать пользователям, отвечать на их вопросы и поддерживать дружелюбную беседу.
Отвечай кратко и по существу, но дружелюбно. Используй emoji для большей выразительности, но умеренно."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.message_service = MessageService(session)
        self.giga_client = GigaChatClient()
    
    async def generate_response(
        self,
        user_id: int,
        user_message: str,
        context_limit: int = 10
    ) -> str:
        try:
            await self.message_service.add_message(
                user_id=user_id,
                role=MessageRole.USER,
                content=user_message
            )
            
            messages = await self._prepare_context(user_id, context_limit)
            ai_response = await self.giga_client.generate_response(messages)
            
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
        limit: int
    ) -> list[dict[str, str]]:
        history = await self.message_service.get_user_messages(user_id, limit)
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]
        
        for msg in reversed(history):
            role = "user" if msg.role == MessageRole.USER else "assistant"
            messages.append({
                "role": role,
                "content": msg.content
            })
        
        return messages
    
    async def clear_history(self, user_id: int) -> int:
        return await self.message_service.clear_user_messages(user_id)
