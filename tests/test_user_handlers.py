import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from aiogram.types import Message

from bot.handlers import user as user_handlers


@pytest.mark.asyncio
class TestStartCommand:
    
    async def test_start_command_existing_user(
        self,
        create_mock_message,
        mock_session,
        mock_user_service
    ):
        message = create_mock_message(text="/start")
        
        with patch('bot.handlers.user.UserService', return_value=mock_user_service):
            await user_handlers.cmd_start(message, mock_session)
        
        mock_user_service.get_user.assert_called_once_with(message.from_user.id)
        
        message.answer.assert_called_once()
        call_args = message.answer.call_args[0][0]
        assert "Привет" in call_args
        assert "AI-ассистент" in call_args
    
    async def test_start_command_new_user(
        self,
        create_mock_message,
        mock_session
    ):
        message = create_mock_message(text="/start")
        mock_service = AsyncMock()
        mock_service.get_user = AsyncMock(return_value=None)
        
        with patch('bot.handlers.user.UserService', return_value=mock_service):
            await user_handlers.cmd_start(message, mock_session)
        
        message.answer.assert_called_once()
        call_args = message.answer.call_args[0][0]
        assert "незнакомец" in call_args or "Привет" in call_args


@pytest.mark.asyncio
class TestHelpCommand:
    
    async def test_help_command(self, create_mock_message):
        message = create_mock_message(text="/help")
        
        await user_handlers.cmd_help(message)
        
        message.answer.assert_called_once()
        call_args = message.answer.call_args
        
        assert "Доступные команды" in call_args[0][0]
        assert "/start" in call_args[0][0]
        assert "/help" in call_args[0][0]
        assert "/reset" in call_args[0][0]
        
        assert call_args[1]["parse_mode"] == "HTML"


@pytest.mark.asyncio
class TestAboutCommand:
    
    async def test_about_command(self, create_mock_message):
        message = create_mock_message(text="/about")
        
        await user_handlers.cmd_about(message)
        
        message.answer.assert_called_once()
        call_args = message.answer.call_args
        
        assert "О боте" in call_args[0][0]
        assert "GigaChat" in call_args[0][0]
        assert "Python" in call_args[0][0]
        
        assert call_args[1]["parse_mode"] == "HTML"


@pytest.mark.asyncio
class TestResetCommand:
    
    async def test_reset_command_success(
        self,
        create_mock_message,
        mock_session,
        mock_user_service,
        mock_ai_service
    ):
        message = create_mock_message(text="/reset")
        
        with patch('bot.handlers.user.UserService', return_value=mock_user_service), \
             patch('bot.handlers.user.AIService', return_value=mock_ai_service):
            await user_handlers.cmd_reset(message, mock_session)
        
        mock_user_service.get_user.assert_called_once()
        mock_ai_service.clear_history.assert_called_once()
        
        message.answer.assert_called_once()
        call_args = message.answer.call_args[0][0]
        assert "История диалога очищена" in call_args
        assert "Удалено сообщений: 5" in call_args
    
    async def test_reset_command_user_not_found(
        self,
        create_mock_message,
        mock_session
    ):
        message = create_mock_message(text="/reset")
        
        mock_service = AsyncMock()
        mock_service.get_user = AsyncMock(return_value=None)
        
        with patch('bot.handlers.user.UserService', return_value=mock_service):
            await user_handlers.cmd_reset(message, mock_session)
        
        message.answer.assert_called_once()
        call_args = message.answer.call_args[0][0]
        assert "Ошибка" in call_args
        assert "пользователь не найден" in call_args


@pytest.mark.asyncio
class TestTextMessageHandler:
    
    async def test_handle_text_message_success(
        self,
        create_mock_message,
        mock_session,
        mock_user_service,
        mock_ai_service,
        mock_bot
    ):
        message = create_mock_message(text="Привет, как дела?")
        message.bot = mock_bot
        
        with patch('bot.handlers.user.UserService', return_value=mock_user_service), \
             patch('bot.handlers.user.AIService', return_value=mock_ai_service), \
             patch('bot.handlers.user.markdown_to_html', return_value="<b>Тестовый ответ от AI</b>"):
            
            await user_handlers.handle_text_message(message, mock_session)
        
        mock_bot.send_chat_action.assert_called_once_with(message.chat.id, "typing")
        
        mock_user_service.get_user.assert_called_once()
        mock_ai_service.generate_response.assert_called_once()
        
        message.answer.assert_called()
    
    async def test_handle_text_message_user_not_found(
        self,
        create_mock_message,
        mock_session,
        mock_bot
    ):
        message = create_mock_message(text="Тестовое сообщение")
        message.bot = mock_bot
        
        mock_service = AsyncMock()
        mock_service.get_user = AsyncMock(return_value=None)
        
        with patch('bot.handlers.user.UserService', return_value=mock_service):
            await user_handlers.handle_text_message(message, mock_session)
        
        message.answer.assert_called_once()
        call_args = message.answer.call_args[0][0]
        assert "Ошибка" in call_args
        assert "пользователь не найден" in call_args
    
    async def test_handle_text_message_long_response(
        self,
        create_mock_message,
        mock_session,
        mock_user_service,
        mock_ai_service,
        mock_bot
    ):
        message = create_mock_message(text="Расскажи длинную историю")
        message.bot = mock_bot
        
        long_response = "A" * 5000
        
        with patch('bot.handlers.user.UserService', return_value=mock_user_service), \
             patch('bot.handlers.user.AIService', return_value=mock_ai_service), \
             patch('bot.handlers.user.markdown_to_html', return_value=long_response):
            
            await user_handlers.handle_text_message(message, mock_session)
        
        assert message.answer.call_count >= 2


@pytest.mark.asyncio
class TestInvalidMessageHandler:
    
    async def test_handle_too_long_message(self, create_mock_message):
        long_text = "A" * 4001
        message = create_mock_message(text=long_text)
        
        await user_handlers.handle_invalid_message(message)
        
        message.answer.assert_called_once()
        call_args = message.answer.call_args[0][0]
        assert "слишком длинное" in call_args
        assert "4000" in call_args
    
    async def test_handle_empty_message(self, create_mock_message):
        message = create_mock_message(text="   ")
        
        await user_handlers.handle_invalid_message(message)
        
        message.answer.assert_called_once()
        call_args = message.answer.call_args[0][0]
        assert "не может быть пустым" in call_args
    
    async def test_handle_banned_content(self, create_mock_message):
        message = create_mock_message(text="Обычное сообщение")
        
        await user_handlers.handle_invalid_message(message)
        
        message.answer.assert_called_once()
        call_args = message.answer.call_args[0][0]
        assert "нежелательный контент" in call_args
