from pydantic import BaseModel

from .bot import BotConfig
from .redis import RedisConfig
from .database import DatabaseConfig


class Settings(BaseModel):
    bot: BotConfig = BotConfig()
    redis: RedisConfig = RedisConfig()
    db: DatabaseConfig = DatabaseConfig()


settings = Settings()