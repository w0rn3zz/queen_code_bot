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
        
        log_file_path = logs_dir / "bot.log"

        def timetz(*args):
            tz = timezone("Europe/Moscow")
            return datetime.now(tz).timetuple()

        logging.Formatter.converter = timetz
        
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        file_handler = logging.FileHandler(
            log_file_path,
            mode="a",
            encoding="utf-8",
        )
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

        logging.getLogger("aiogram").setLevel(logging.WARNING)
        logging.getLogger("httpx").setLevel(logging.WARNING)

        logging.info("Логирование настроено")
        logging.info(f"Файл логов: {log_file_path}")

    def setup_routers(self):
        from bot.handlers import user, admin
        self.dp.include_routers(admin.router, user.router)

        
        logging.info("Роутеры подключены")

    def setup_middlewares(self):
        from middlewares.inject_session import InjectSession
        from middlewares.update_user import UpdateUser
        from middlewares.antiflood import AntiFloodMiddleware
        from middlewares.logging_middleware import LoggingMiddleware
        from core.db_helper import db_helper
        
        self.dp.update.outer_middleware(InjectSession(db_helper))
        self.dp.update.outer_middleware(UpdateUser())
        self.dp.message.middleware(LoggingMiddleware())
        self.dp.message.middleware(AntiFloodMiddleware(time_limit=1))
        
        logging.info("Middleware подключены")

    async def shutdown(self):
        from core.db_helper import db_helper
        
        await db_helper.dispose()
        logging.info("🛑 Завершение работы бота...")