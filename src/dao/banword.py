from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import BanWord
from .base import BaseDao


class BanWordDao(BaseDao[BanWord]):
    model = BanWord

    async def get_all_active(self) -> list[str]:
        query = select(self.model.word).where(self.model.is_active == True)
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def add_words(self, words: list[str]) -> list[BanWord]:
        ban_words = []
        for word in words:
            existing = await self.find_one_by_filters({"word": word.lower().strip()})
            if not existing:
                ban_word = await self.create({"word": word.lower().strip()})
                ban_words.append(ban_word)
            else:
                if not existing.is_active:
                    await self.update({"id": existing.id}, {"is_active": True})
                ban_words.append(existing)
        return ban_words
    
    async def remove_word(self, word: str) -> bool:
        updated = await self.update({"word": word.lower().strip()}, {"is_active": False})
        return updated is not None
    
    async def activate_word(self, word: str) -> bool:
        updated = await self.update({"word": word.lower().strip()}, {"is_active": True})
        return updated is not None
    
    async def delete_word(self, word: str) -> bool:
        ban_word = await self.find_one_by_filters({"word": word.lower().strip()})
        if ban_word:
            await self.session.delete(ban_word)
            await self.session.flush()
            return True
        return False
