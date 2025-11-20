import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from core.config import settings

from utils.setup import SetupManager


async def main():
    redis = Redis(host=settings.redis.redis_host, port=settings.redis.redis_port)
    storage = RedisStorage(
        redis=redis, key_builder=DefaultKeyBuilder(with_destiny=True)
    )

    bot = Bot(token=settings.bot.bot_token)
    dp = Dispatcher(storage=storage)

    setup_manager = SetupManager(dp)

    dp.startup.register(setup_manager.setup)
    dp.shutdown.register(setup_manager.shutdown)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())