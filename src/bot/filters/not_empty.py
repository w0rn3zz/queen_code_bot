from aiogram.filters import Filter
from aiogram.types import Message


class NotEmptyFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        if not message.text:
            return False
        return bool(message.text.strip())
