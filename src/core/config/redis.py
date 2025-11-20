from .base import BaseConfig

class RedisConfig(BaseConfig):
    redis_host: str
    redis_port: int