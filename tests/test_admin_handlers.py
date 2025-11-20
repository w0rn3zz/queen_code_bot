import pytest
from unittest.mock import AsyncMock, MagicMock, patch, Mock
from io import BytesIO

from aiogram.types import Message, Document, File

from bot.handlers import admin as admin_handlers


@pytest.mark.asyncio
class TestAdminCommand:
    
    async def test_admin_command_panel(self, create_mock_message, mock_admin_user):
        message = create_mock_message(text="/admin", user=mock_admin_user)
        
        await admin_handlers.cmd_admin(message)
        
        message.answer.assert_called_once()
        call_args = message.answer.call_args
        
        text = call_args[0][0]
        assert "Панель администратора" in text
        assert "банворд" in text.lower()
        assert "администратор" in text.lower()
        assert call_args[1]["parse_mode"] == "HTML"


@pytest.mark.asyncio
class TestBanwordsList:
    
    async def test_list_banwords_with_words(
        self,
        create_mock_message,
        mock_admin_user,
        mock_session,
        mock_banword_service
    ):
        message = create_mock_message(text="/banwords_list", user=mock_admin_user)
        
        with patch('bot.handlers.admin.BanWordService', return_value=mock_banword_service):
            await admin_handlers.cmd_list_banwords(message, mock_session)
        
        mock_banword_service.get_all_words.assert_called_once()
        message.answer.assert_called_once()
        
        call_args = message.answer.call_args[0][0]
        assert "банворд" in call_args.lower()
    
    async def test_list_banwords_empty(
        self,
        create_mock_message,
        mock_admin_user,
        mock_session
    ):
        message = create_mock_message(text="/banwords_list", user=mock_admin_user)
        
        mock_service = AsyncMock()
        mock_service.get_all_words = AsyncMock(return_value=[])
        
        with patch('bot.handlers.admin.BanWordService', return_value=mock_service):
            await admin_handlers.cmd_list_banwords(message, mock_session)
        
        message.answer.assert_called_once()
        call_args = message.answer.call_args[0][0]
        assert "пуст" in call_args


@pytest.mark.asyncio
class TestAddBanword:
    
    async def test_add_banword_success(
        self,
        create_mock_message,
        mock_admin_user,
        mock_session,
        mock_banword_service
    ):
        message = create_mock_message(text="/add_banword спам", user=mock_admin_user)
        
        with patch('bot.handlers.admin.BanWordService', return_value=mock_banword_service):
            await admin_handlers.cmd_add_banword(message, mock_session)
        
        mock_banword_service.add_word.assert_called_once_with("спам")
        message.answer.assert_called_once()
        
        call_args = message.answer.call_args[0][0]
        assert "добавлено" in call_args.lower()
        assert "спам" in call_args
    
    async def test_add_banword_no_argument(
        self,
        create_mock_message,
        mock_admin_user,
        mock_session
    ):
        message = create_mock_message(text="/add_banword", user=mock_admin_user)
        
        mock_service = AsyncMock()
        
        with patch('bot.handlers.admin.BanWordService', return_value=mock_service):
            await admin_handlers.cmd_add_banword(message, mock_session)
        
        message.answer.assert_called_once()
        call_args = message.answer.call_args[0][0]
        assert "Использование" in call_args
        
        mock_service.add_word.assert_not_called()


@pytest.mark.asyncio
class TestAddBanwords:
    
    async def test_add_multiple_banwords(
        self,
        create_mock_message,
        mock_admin_user,
        mock_session,
        mock_banword_service
    ):
        message = create_mock_message(
            text="/add_banwords спам реклама мошенничество",
            user=mock_admin_user
        )
        
        with patch('bot.handlers.admin.BanWordService', return_value=mock_banword_service):
            await admin_handlers.cmd_add_banwords(message, mock_session)
        
        mock_banword_service.add_words_from_text.assert_called_once()
        message.answer.assert_called_once()
        
        call_args = message.answer.call_args[0][0]
        assert "Обработано" in call_args
        assert "5" in call_args
        assert "10" in call_args


@pytest.mark.asyncio
class TestRemoveBanword:
    
    async def test_remove_banword_success(
        self,
        create_mock_message,
        mock_admin_user,
        mock_session,
        mock_banword_service
    ):
        message = create_mock_message(text="/remove_banword спам", user=mock_admin_user)
        
        with patch('bot.handlers.admin.BanWordService', return_value=mock_banword_service):
            await admin_handlers.cmd_remove_banword(message, mock_session)
        
        mock_banword_service.remove_word.assert_called_once_with("спам")
        message.answer.assert_called_once()
        
        call_args = message.answer.call_args[0][0]
        assert "деактивировано" in call_args.lower()
    
    async def test_remove_banword_not_found(
        self,
        create_mock_message,
        mock_admin_user,
        mock_session
    ):
        message = create_mock_message(text="/remove_banword несуществует", user=mock_admin_user)
        
        mock_service = AsyncMock()
        mock_service.remove_word = AsyncMock(return_value=False)
        
        with patch('bot.handlers.admin.BanWordService', return_value=mock_service):
            await admin_handlers.cmd_remove_banword(message, mock_session)
        
        message.answer.assert_called_once()
        call_args = message.answer.call_args[0][0]
        assert "не найдено" in call_args.lower()


@pytest.mark.asyncio
class TestDeleteBanword:
    
    async def test_delete_banword_success(
        self,
        create_mock_message,
        mock_admin_user,
        mock_session,
        mock_banword_service
    ):
        message = create_mock_message(text="/delete_banword спам", user=mock_admin_user)
        
        with patch('bot.handlers.admin.BanWordService', return_value=mock_banword_service):
            await admin_handlers.cmd_delete_banword(message, mock_session)
        
        mock_banword_service.delete_word.assert_called_once_with("спам")
        message.answer.assert_called_once()
        
        call_args = message.answer.call_args[0][0]
        assert "удалено" in call_args.lower()


@pytest.mark.asyncio
class TestDocumentHandler:
    
    async def test_handle_txt_document(
        self,
        create_mock_message,
        mock_admin_user,
        mock_session,
        mock_banword_service,
        mock_bot
    ):
        
        mock_document = MagicMock(spec=Document)
        mock_document.file_id = "test_file_id"
        mock_document.file_name = "banwords.txt"
        
        message = create_mock_message(user=mock_admin_user)
        message.document = mock_document
        message.bot = mock_bot
        
        # Мок файла
        mock_file = MagicMock(spec=File)
        mock_file.file_path = "documents/banwords.txt"
        mock_bot.get_file = AsyncMock(return_value=mock_file)
        
        file_content = BytesIO(b"spam\nscam\nadvertising")
        mock_bot.download_file = AsyncMock(return_value=file_content)
        
        with patch('bot.handlers.admin.BanWordService', return_value=mock_banword_service):
            await admin_handlers.handle_document(message, mock_session)
        
        mock_bot.get_file.assert_called_once_with("test_file_id")
        mock_banword_service.add_words_from_text.assert_called_once()
        message.answer.assert_called_once()
        
        call_args = message.answer.call_args[0][0]
        assert "обработан" in call_args.lower()
    
    async def test_handle_non_txt_document(
        self,
        create_mock_message,
        mock_admin_user,
        mock_session
    ):
        mock_document = MagicMock(spec=Document)
        mock_document.file_name = "banwords.pdf"
        
        message = create_mock_message(user=mock_admin_user)
        message.document = mock_document
        
        await admin_handlers.handle_document(message, mock_session)
        
        message.answer.assert_called_once()
        call_args = message.answer.call_args[0][0]
        assert ".txt" in call_args


@pytest.mark.asyncio
class TestAdminsList:
    
    async def test_list_admins(
        self,
        create_mock_message,
        mock_admin_user,
        mock_session,
        mock_admin_service
    ):
        message = create_mock_message(text="/admins_list", user=mock_admin_user)
        
        with patch('bot.handlers.admin.AdminService', return_value=mock_admin_service):
            await admin_handlers.cmd_list_admins(message, mock_session)
        
        mock_admin_service.get_all_admins.assert_called_once()
        message.answer.assert_called_once()
        
        call_args = message.answer.call_args[0][0]
        assert "администратор" in call_args.lower()


@pytest.mark.asyncio
class TestAddAdmin:
    
    async def test_add_admin_success(
        self,
        create_mock_message,
        mock_admin_user,
        mock_session,
        mock_admin_service
    ):
        message = create_mock_message(text="/add_admin 123456789", user=mock_admin_user)
        
        mock_admin_service.is_admin = AsyncMock(return_value=False)
        
        with patch('bot.handlers.admin.AdminService', return_value=mock_admin_service):
            await admin_handlers.cmd_add_admin(message, mock_session)
        
        mock_admin_service.add_admin.assert_called_once()
        message.answer.assert_called_once()
        
        call_args = message.answer.call_args[0][0]
        assert "добавлен" in call_args.lower()
    
    async def test_add_admin_already_exists(
        self,
        create_mock_message,
        mock_admin_user,
        mock_session
    ):
        message = create_mock_message(text="/add_admin 123456789", user=mock_admin_user)
        
        mock_service = AsyncMock()
        mock_service.is_admin = AsyncMock(return_value=True)
        
        with patch('bot.handlers.admin.AdminService', return_value=mock_service):
            await admin_handlers.cmd_add_admin(message, mock_session)
        
        message.answer.assert_called_once()
        call_args = message.answer.call_args[0][0]
        assert "уже является" in call_args.lower()
        
        mock_service.add_admin.assert_not_called()
    
    async def test_add_admin_invalid_id(
        self,
        create_mock_message,
        mock_admin_user,
        mock_session
    ):
        message = create_mock_message(text="/add_admin not_a_number", user=mock_admin_user)
        
        mock_service = AsyncMock()
        
        with patch('bot.handlers.admin.AdminService', return_value=mock_service):
            await admin_handlers.cmd_add_admin(message, mock_session)
        
        message.answer.assert_called_once()
        call_args = message.answer.call_args[0][0]
        assert "должно быть числом" in call_args.lower()


@pytest.mark.asyncio
class TestRemoveAdmin:
    
    async def test_remove_admin_success(
        self,
        create_mock_message,
        mock_admin_user,
        mock_session,
        mock_admin_service
    ):
        message = create_mock_message(text="/remove_admin 123456789", user=mock_admin_user)
        
        with patch('bot.handlers.admin.AdminService', return_value=mock_admin_service), \
             patch('bot.handlers.admin.settings.bot.admin_id', 999999999):
            await admin_handlers.cmd_remove_admin(message, mock_session)
        
        mock_admin_service.remove_admin.assert_called_once_with(123456789)
        message.answer.assert_called_once()
        
        call_args = message.answer.call_args[0][0]
        assert "удален" in call_args.lower()
    
    async def test_remove_admin_not_found(
        self,
        create_mock_message,
        mock_admin_user,
        mock_session
    ):
        message = create_mock_message(text="/remove_admin 123456789", user=mock_admin_user)
        
        mock_service = AsyncMock()
        mock_service.remove_admin = AsyncMock(return_value=False)
        
        with patch('bot.handlers.admin.AdminService', return_value=mock_service), \
             patch('bot.handlers.admin.settings.bot.admin_id', 999999999):
            await admin_handlers.cmd_remove_admin(message, mock_session)
        
        message.answer.assert_called_once()
        call_args = message.answer.call_args[0][0]
        assert "не является" in call_args.lower()
    
    async def test_remove_main_admin(
        self,
        create_mock_message,
        mock_admin_user,
        mock_session
    ):
        message = create_mock_message(text="/remove_admin 999999999", user=mock_admin_user)
        
        mock_service = AsyncMock()
        
        with patch('bot.handlers.admin.AdminService', return_value=mock_service), \
             patch('bot.handlers.admin.settings.bot.admin_id', 999999999):
            await admin_handlers.cmd_remove_admin(message, mock_session)
        
        message.answer.assert_called_once()
        call_args = message.answer.call_args[0][0]
        assert "главного" in call_args.lower()
        
        mock_service.remove_admin.assert_not_called()
