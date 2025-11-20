from sqlalchemy.ext.asyncio import AsyncSession

from dao import BanWordDao
from core.models import BanWord


class BanWordService:
    def __init__(self, session: AsyncSession):
        self.dao = BanWordDao(session)
    
    async def get_all_active_words(self) -> list[str]:
        return await self.dao.get_all_active()
    
    async def add_words_from_list(self, words: list[str]) -> tuple[int, int]:
        clean_words = [w.strip() for w in words if w.strip()]
        added = await self.dao.add_words(clean_words)
        return len(added), len(clean_words)
    
    async def add_words_from_text(self, text: str) -> tuple[int, int]:
        import re
        words = re.split(r'[,\s\n]+', text)
        return await self.add_words_from_list(words)
    
    async def add_word(self, word: str) -> BanWord | None:
        words = await self.dao.add_words([word])
        return words[0] if words else None
    
    async def remove_word(self, word: str) -> bool:
        return await self.dao.remove_word(word)
    
    async def activate_word(self, word: str) -> bool:
        return await self.dao.activate_word(word)
    
    async def delete_word(self, word: str) -> bool:
        return await self.dao.delete_word(word)
    
    async def get_all_words(self) -> list[BanWord]:
        return await self.dao.find_all()
