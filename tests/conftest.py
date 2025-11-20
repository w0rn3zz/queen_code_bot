
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from typing import AsyncGenerator

from aiogram import Bot, Dispatcher
from aiogram.types import User, Chat, Message, Update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_session() -> AsyncMock:
    session = AsyncMock(spec=AsyncSession)
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    return session


@pytest.fixture
def mock_bot() -> MagicMock:
    bot = MagicMock(spec=Bot)
    bot.send_message = AsyncMock()
    bot.send_chat_action = AsyncMock()
    bot.get_file = AsyncMock()
    bot.download_file = AsyncMock()
    return bot


@pytest.fixture
def mock_user() -> User:
    return User(
        id=123456789,
        is_bot=False,
        first_name="Test",
        last_name="User",
        username="testuser",
        language_code="ru"
    )


@pytest.fixture
def mock_admin_user() -> User:
    return User(
        id=987654321,
        is_bot=False,
        first_name="Admin",
        last_name="User",
        username="adminuser",
        language_code="ru"
    )


@pytest.fixture
def mock_chat() -> Chat:
    return Chat(
        id=123456789,
        type="private"
    )


@pytest.fixture
def create_mock_message(mock_bot, mock_user, mock_chat):
    def _create_message(
        text: str = "Test message",
        user: User = None,
        chat: Chat = None,
        message_id: int = 1,
        document = None,
        bot = None
    ) -> MagicMock:
        msg = MagicMock(spec=Message)
        msg.message_id = message_id
        msg.date = 1234567890
        msg.chat = chat or mock_chat
        msg.from_user = user or mock_user
        msg.text = text
        msg.bot = bot or mock_bot
        msg.document = document
        msg.answer = AsyncMock()
        msg.reply = AsyncMock()
        return msg
    return _create_message


@pytest.fixture
def mock_user_service() -> AsyncMock:
    service = AsyncMock()
    
    mock_user_model = MagicMock()
    mock_user_model.id = 1
    mock_user_model.tg_id = 123456789
    mock_user_model.username = "testuser"
    mock_user_model.first_name = "Test"
    mock_user_model.last_name = "User"
    
    service.get_user = AsyncMock(return_value=mock_user_model)
    service.create_user = AsyncMock(return_value=mock_user_model)
    service.update_user = AsyncMock(return_value=mock_user_model)
    service.upsert_user = AsyncMock(return_value=mock_user_model)
    
    return service


@pytest.fixture
def mock_ai_service() -> AsyncMock:
    service = AsyncMock()
    service.generate_response = AsyncMock(return_value="Тестовый ответ от AI")
    service.clear_history = AsyncMock(return_value=5)
    return service


@pytest.fixture
def mock_banword_service() -> AsyncMock:
    service = AsyncMock()
    
    mock_banword = MagicMock()
    mock_banword.word = "testword"
    mock_banword.is_active = True
    
    service.get_all_words = AsyncMock(return_value=[mock_banword])
    service.add_word = AsyncMock()
    service.add_words_from_text = AsyncMock(return_value=(5, 10))
    service.remove_word = AsyncMock(return_value=True)
    service.delete_word = AsyncMock(return_value=True)
    service.is_banned = AsyncMock(return_value=False)
    
    return service


@pytest.fixture
def mock_admin_service() -> AsyncMock:
    service = AsyncMock()
    
    mock_admin = MagicMock()
    mock_admin.tg_id = 987654321
    
    service.get_all_admins = AsyncMock(return_value=[mock_admin])
    service.is_admin = AsyncMock(return_value=True)
    service.add_admin = AsyncMock()
    service.remove_admin = AsyncMock(return_value=True)
    
    return service


@pytest.fixture
def mock_message_service() -> AsyncMock:
    service = AsyncMock()
    service.add_message = AsyncMock()
    service.get_user_messages = AsyncMock(return_value=[])
    service.clear_user_messages = AsyncMock(return_value=5)
    return service
