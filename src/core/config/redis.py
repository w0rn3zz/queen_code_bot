from .base import BaseCofing

class RedisConfig(BaseCofing):
    redis_host: str
    redis_port: int