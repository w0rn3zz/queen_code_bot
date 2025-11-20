import re
from aiogram.filters import Filter
from aiogram.types import Message


class ContentFilter(Filter):
    
    BLACKLIST_WORDS = {
        "бля", "блять", "хуй", "пизд", "ебан", "еба", "ёб", "сука", "суки",
        "гандон", "шлюх", "мудак", "мудил", "дебил", "уёб", "уеб",
        "убить", "убью", "убей", "смерть", "терракт", "теракт", "взрыв",
        "расстрел", "фашист", "нацист",
        "наркотик", "наркота", "героин", "кокаин", "марихуан", "гашиш",
        "синтетик", "соль", "спайс", "мефедрон",
    }
    
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
    
    async def __call__(self, message: Message) -> bool:
        if not message.text:
            return True
        
        text = message.text.lower()
        normalized_text = self._normalize_text(text)
        
        if self._contains_blacklisted_words(normalized_text):
            return False
        
        if self._is_spam(text):
            return False
        
        return True
    
    def _normalize_text(self, text: str) -> str:
        normalized = text
        for pattern, replacement in self.OBFUSCATION_PATTERNS:
            normalized = re.sub(pattern, replacement, normalized)
        return normalized
    
    def _contains_blacklisted_words(self, text: str) -> bool:
        words = re.findall(r'\w+', text)
        
        for word in words:
            for blacklisted in self.BLACKLIST_WORDS:
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
