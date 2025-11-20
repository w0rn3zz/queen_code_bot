from aiogram.filters import Filter
from aiogram.types import Message


class MessageLengthFilter(Filter):
    def __init__(self, max_length: int = 4000):
        self.max_length = max_length
    
    async def __call__(self, message: Message) -> bool:
        if not message.text:
            return False
        return len(message.text) <= self.max_length
