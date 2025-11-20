from .base import BaseConfig


class AIConfig(BaseConfig):
    giga_chat_api_key: str
    temperature: float = 0.7
    max_tokens: int = 2048
    context_limit: int = 6
    system_prompt: str = """Ты — полезный AI-ассистент.

СТРОГИЕ ПРАВИЛА:
1. Внимательно читай запрос пользователя
2. Отвечай ТОЧНО на то, что спрашивают
3. Если просят код на конкретном языке - давай код именно на этом языке
4. Не меняй тему, не предлагай альтернативы без запроса
5. Будь конкретным и точным"""