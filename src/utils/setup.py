import logging
import os
from datetime import datetime
from pathlib import Path

from pytz import timezone
from aiogram import Dispatcher

from core.config import settings


class SetupManager:
    """Менеджер настройки и инициализации бота"""

    def __init__(self, dp: Dispatcher):
        self.dp = dp

    async def setup(self):
        self.setup_logging()
        self.setup_routers()
        self.setup_middlewares()

    def setup_logging(self):
        logs_dir = Path(__file__).resolve().parents[2] / "logs"
        logs_dir.mkdir(exist_ok=True)

        file_log = logging.FileHandler(
            logs_dir / "bot.log",
            mode="a",
            encoding="utf-8",
        )
        file_log.setLevel(logging.ERROR)

        console_out = logging.StreamHandler()
        console_out.setLevel(logging.INFO)

        def timetz(*args):
            tz = timezone("Europe/Moscow")
            return datetime.now(tz).timetuple()

        logging.Formatter.converter = timetz

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[file_log, console_out],
        )

        logging.getLogger("aiogram").setLevel(logging.WARNING)
        logging.getLogger("httpx").setLevel(logging.WARNING)

        logging.info("✅ Логирование настроено")

    def setup_routers(self):
        from bot.handlers import user
        self.dp.include_routers(user.router)

        
        logging.info("✅ Роутеры подключены")

    def setup_middlewares(self):
        from middlewares.inject_session import InjectSession
        from middlewares.update_user import UpdateUser
        from core.db_helper import db_helper
        
        self.dp.update.outer_middleware(InjectSession(db_helper))
        self.dp.update.outer_middleware(UpdateUser())
        
        logging.info("✅ Middleware подключены")

    async def shutdown(self):
        from core.db_helper import db_helper
        
        await db_helper.dispose()
        logging.info("🛑 Завершение работы бота...")