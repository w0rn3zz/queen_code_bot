import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseCofing(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=os.getenv("ENV_FILE", ".env"),
        case_sensitive=False
    )
