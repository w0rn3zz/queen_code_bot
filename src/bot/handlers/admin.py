from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, Document
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from services import BanWordService, AdminService, UserService
from bot.filters import IsAdminFilter
from core.config import settings

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("admin"), IsAdminFilter())
async def cmd_admin(message: Message):
    admin_text = """
🔐 <b>Панель администратора</b>

📝 <b>Управление банвордами:</b>
/banwords_list - Показать все банворды
/add_banword &lt;слово&gt; - Добавить одно слово
/add_banwords &lt;слова&gt; - Добавить несколько слов (через пробел или запятую)
/remove_banword &lt;слово&gt; - Деактивировать слово
/delete_banword &lt;слово&gt; - Удалить слово полностью

👥 <b>Управление администраторами:</b>
/admins_list - Список всех администраторов
/add_admin &lt;telegram_id&gt; - Добавить админа
/remove_admin &lt;telegram_id&gt; - Удалить админа

📄 <b>Загрузка файла:</b>
Отправь .txt файл с банвордами (каждое слово с новой строки)
"""
    await message.answer(admin_text, parse_mode="HTML")


@router.message(Command("banwords_list"), IsAdminFilter())
async def cmd_list_banwords(message: Message, session: AsyncSession):
    banword_service = BanWordService(session)
    all_words = await banword_service.get_all_words()
    
    if not all_words:
        await message.answer("📋 Список банвордов пуст")
        return
    
    active_words = [w for w in all_words if w.is_active]
    inactive_words = [w for w in all_words if not w.is_active]
    
    text = f"📋 <b>Всего банвордов: {len(all_words)}</b>\n\n"
    
    if active_words:
        text += f"✅ <b>Активные ({len(active_words)}):</b>\n"
        words_list = ", ".join([w.word for w in active_words[:50]])
        text += f"<code>{words_list}</code>\n"
        if len(active_words) > 50:
            text += f"<i>... и еще {len(active_words) - 50}</i>\n"
        text += "\n"
    
    if inactive_words:
        text += f"❌ <b>Неактивные ({len(inactive_words)}):</b>\n"
        words_list = ", ".join([w.word for w in inactive_words[:20]])
        text += f"<code>{words_list}</code>\n"
        if len(inactive_words) > 20:
            text += f"<i>... и еще {len(inactive_words) - 20}</i>\n"
    
    await message.answer(text, parse_mode="HTML")


@router.message(Command("add_banword"), IsAdminFilter())
async def cmd_add_banword(message: Message, session: AsyncSession):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("❌ Использование: /add_banword <слово>")
        return
    
    word = args[1].strip()
    banword_service = BanWordService(session)
    
    try:
        await banword_service.add_word(word)
        await message.answer(f"✅ Слово <code>{word}</code> добавлено в банлист", parse_mode="HTML")
    except Exception as e:
        logger.error(f"Error adding banword: {e}")
        await message.answer(f"❌ Ошибка при добавлении слова")


@router.message(Command("add_banwords"), IsAdminFilter())
async def cmd_add_banwords(message: Message, session: AsyncSession):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("❌ Использование: /add_banwords <слова через пробел или запятую>")
        return
    
    text = args[1]
    banword_service = BanWordService(session)
    
    try:
        added, total = await banword_service.add_words_from_text(text)
        await message.answer(
            f"✅ Обработано слов: {total}\n"
            f"➕ Добавлено новых: {added}",
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Error adding banwords: {e}")
        await message.answer(f"❌ Ошибка при добавлении слов")


@router.message(Command("remove_banword"), IsAdminFilter())
async def cmd_remove_banword(message: Message, session: AsyncSession):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("❌ Использование: /remove_banword <слово>")
        return
    
    word = args[1].strip()
    banword_service = BanWordService(session)
    
    try:
        result = await banword_service.remove_word(word)
        if result:
            await message.answer(f"✅ Слово <code>{word}</code> деактивировано", parse_mode="HTML")
        else:
            await message.answer(f"❌ Слово <code>{word}</code> не найдено", parse_mode="HTML")
    except Exception as e:
        logger.error(f"Error removing banword: {e}")
        await message.answer(f"❌ Ошибка при деактивации слова")


@router.message(Command("delete_banword"), IsAdminFilter())
async def cmd_delete_banword(message: Message, session: AsyncSession):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("❌ Использование: /delete_banword <слово>")
        return
    
    word = args[1].strip()
    banword_service = BanWordService(session)
    
    try:
        result = await banword_service.delete_word(word)
        if result:
            await message.answer(f"✅ Слово <code>{word}</code> удалено из базы", parse_mode="HTML")
        else:
            await message.answer(f"❌ Слово <code>{word}</code> не найдено", parse_mode="HTML")
    except Exception as e:
        logger.error(f"Error deleting banword: {e}")
        await message.answer(f"❌ Ошибка при удалении слова")


@router.message(F.document, IsAdminFilter())
async def handle_document(message: Message, session: AsyncSession):
    if not message.document:
        return
    
    if not message.document.file_name.endswith('.txt'):
        await message.answer("❌ Пожалуйста, отправьте .txt файл")
        return
    
    try:
        from aiogram import Bot
        bot: Bot = message.bot
        file = await bot.get_file(message.document.file_id)
        file_content = await bot.download_file(file.file_path)
        
        content = file_content.read().decode('utf-8')
        
        banword_service = BanWordService(session)
        added, total = await banword_service.add_words_from_text(content)
        
        await message.answer(
            f"✅ Файл обработан!\n"
            f"📊 Обработано слов: {total}\n"
            f"➕ Добавлено новых: {added}",
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        await message.answer("❌ Ошибка при обработке файла")


@router.message(Command("admins_list"), IsAdminFilter())
async def cmd_list_admins(message: Message, session: AsyncSession):
    admin_service = AdminService(session)
    admins = await admin_service.get_all_admins()
    
    text = "👥 <b>Список администраторов:</b>\n\n"
    text += f"🔑 <b>Главный админ:</b> <code>{settings.bot.admin_id}</code>\n\n"
    
    if admins:
        text += f"👤 <b>Дополнительные администраторы ({len(admins)}):</b>\n"
        for admin in admins:
            text += f"• ID: <code>{admin.tg_id}</code>\n"
    else:
        text += "<i>Дополнительных администраторов нет</i>"
    
    await message.answer(text, parse_mode="HTML")


@router.message(Command("add_admin"), IsAdminFilter())
async def cmd_add_admin(message: Message, session: AsyncSession):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("❌ Использование: /add_admin <telegram_id>")
        return
    
    try:
        target_user_tg_id = int(args[1].strip())
    except ValueError:
        await message.answer("❌ ID должно быть числом")
        return
    
    admin_service = AdminService(session)
    if await admin_service.is_admin(target_user_tg_id):
        await message.answer("❌ Этот пользователь уже является администратором")
        return
    
    try:
        await admin_service.add_admin(target_user_tg_id, message.from_user.id)
        
        await message.answer(f"✅ Пользователь <code>{target_user_tg_id}</code> добавлен в администраторы", parse_mode="HTML")
    except Exception as e:
        logger.error(f"Error adding admin: {e}")
        await message.answer("❌ Ошибка при добавлении администратора")


@router.message(Command("remove_admin"), IsAdminFilter())
async def cmd_remove_admin(message: Message, session: AsyncSession):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("❌ Использование: /remove_admin <telegram_id>")
        return
    
    try:
        target_user_tg_id = int(args[1].strip())
    except ValueError:
        await message.answer("❌ ID должно быть числом")
        return
    
    if target_user_tg_id == settings.bot.admin_id:
        await message.answer("❌ Нельзя удалить главного администратора")
        return
    
    try:
        admin_service = AdminService(session)
        result = await admin_service.remove_admin(target_user_tg_id)
        
        if result:
            await message.answer(f"✅ Пользователь <code>{target_user_tg_id}</code> удален из администраторов", parse_mode="HTML")
        else:
            await message.answer("❌ Пользователь не является администратором")
    except Exception as e:
        logger.error(f"Error removing admin: {e}")
        await message.answer("❌ Ошибка при удалении администратора")
