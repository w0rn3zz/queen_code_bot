import logging

from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

from core.config import settings


logger = logging.getLogger(__name__)


class GigaChatClient:
    
    def __init__(self):
        self.api_key = settings.ai.giga_chat_api_key
        self._client = None
    
    def _get_client(self) -> GigaChat:
        if self._client is None:
            self._client = GigaChat(
                credentials=self.api_key,
                verify_ssl_certs=False,
                scope="GIGACHAT_API_PERS"
            )
        return self._client
    
    async def generate_response(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1024
    ) -> str:
        try:
            client = self._get_client()
            
            giga_messages = []
            
            for msg in messages:
                if msg["role"] == "system":
                    continue
                elif msg["role"] == "user":
                    giga_messages.append(Messages(role=MessagesRole.USER, content=msg["content"]))
                else:
                    giga_messages.append(Messages(role=MessagesRole.ASSISTANT, content=msg["content"]))
            
            response = client.chat(
                Chat(
                    messages=giga_messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
            )
            
            if response.choices and len(response.choices) > 0:
                full_response = response.choices[0].message.content
                return full_response
            
            logger.error("GigaChat returned empty response")
            return "Извините, не могу сгенерировать ответ. Попробуйте еще раз."
                
        except Exception as e:
            logger.error(f"GigaChat error: {e}")
            return "Произошла ошибка при генерации ответа. Пожалуйста, попробуйте позже."
    
    def close(self):
        if self._client:
            self._client = None
