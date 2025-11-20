import re
from pathlib import Path
from aiogram.filters import Filter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from services import BanWordService


class ContentFilter(Filter):
    
    @staticmethod
    def _load_default_banwords() -> set[str]:
        try:
            banwords_file = Path(__file__).parent / "default_banwords.txt"
            if banwords_file.exists():
                with open(banwords_file, 'r', encoding='utf-8') as f:
                    words = {line.strip() for line in f if line.strip()}
                return words
        except Exception:
            pass
        return {"спам", "реклама", "мошенничество"}
    
    DEFAULT_BLACKLIST_WORDS = _load_default_banwords.__func__()
    
    OBFUSCATION_PATTERNS = [
        (r'[0оo]', 'о'),
        (r'[3з]', 'з'),
        (r'[4ч]', 'ч'),
        (r'[6б]', 'б'),
        (r'[@а]', 'а'),
        (r'[ёе]', 'е'),
        (r'[йi]', 'и'),
    ]
    
    def __init__(self, strict: bool = False):
        self.strict = strict
    
    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        if not message.text:
            return True
        
        banwords = await self._load_banwords(session)
        
        text = message.text.lower()
        normalized_text = self._normalize_text(text)
        
        if self._contains_blacklisted_words(normalized_text, banwords):
            return False
        
        if self._is_spam(text):
            return False
        
        return True
    
    async def _load_banwords(self, session: AsyncSession) -> set[str]:
        try:
            banword_service = BanWordService(session)
            words = await banword_service.get_all_active_words()
            return set(words) if words else self.DEFAULT_BLACKLIST_WORDS
        except Exception:
            return self.DEFAULT_BLACKLIST_WORDS
    
    def _normalize_text(self, text: str) -> str:
        normalized = text
        for pattern, replacement in self.OBFUSCATION_PATTERNS:
            normalized = re.sub(pattern, replacement, normalized)
        return normalized
    
    def _contains_blacklisted_words(self, text: str, blacklist: set[str]) -> bool:
        words = re.findall(r'\w+', text)
        
        for word in words:
            for blacklisted in blacklist:
                if blacklisted in word:
                    return True
        
        return False
    
    def _is_spam(self, text: str) -> bool:
        if re.search(r'(.)\1{9,}', text):
            return True
        
        emoji_count = len(re.findall(r'[^\w\s,.]', text))
        if emoji_count > 20:
            return True
        
        words = text.split()
        if len(words) > 5:
            unique_words = set(words)
            if len(unique_words) / len(words) < 0.3:
                return True
        
        return False
