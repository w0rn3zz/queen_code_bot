from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from services import UserService, AIService
from bot.filters import MessageLengthFilter, NotEmptyFilter

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession):
    user_service = UserService(session)
    user = await user_service.get_user(message.from_user.id)
    
    welcome_text = f"""
👋 Привет, {user.first_name if user else 'незнакомец'}!

Я AI-ассистент, готовый помочь тебе с различными вопросами.

Просто напиши мне что-нибудь, и я постараюсь помочь!

Доступные команды:
/help - Справка по командам
/about - Информация о боте
/reset - Очистить историю диалога
"""
    await message.answer(welcome_text)


@router.message(Command("help"))
async def cmd_help(message: Message):
    help_text = """
📋 <b>Доступные команды:</b>

/start - Начать работу с ботом
/help - Показать эту справку
/about - Информация о боте
/reset - Очистить историю диалога

💬 <b>Как использовать:</b>
Просто отправь мне любое сообщение, и я отвечу на него, используя AI.
Я помню контекст нашего разговора, так что можешь задавать уточняющие вопросы.
"""
    await message.answer(help_text, parse_mode="HTML")


@router.message(Command("about"))
async def cmd_about(message: Message):
    about_text = """
🤖 <b>О боте</b>

Я AI-ассистент на базе GigaChat, созданный для помощи пользователям.

<b>Возможности:</b>
• Отвечаю на вопросы
• Веду диалог с учетом контекста
• Помогаю решать различные задачи

<b>Технологии:</b>
• Python + aiogram
• GigaChat API
• PostgreSQL + Redis
"""
    await message.answer(about_text, parse_mode="HTML")


@router.message(Command("reset"))
async def cmd_reset(message: Message, session: AsyncSession):
    user_service = UserService(session)
    user = await user_service.get_user(message.from_user.id)
    
    if user:
        ai_service = AIService(session)
        deleted_count = await ai_service.clear_history(user.id)
        await message.answer(
            f"✅ История диалога очищена!\n"
            f"Удалено сообщений: {deleted_count}"
        )
    else:
        await message.answer("❌ Ошибка: пользователь не найден.")


@router.message(F.text, NotEmptyFilter(), MessageLengthFilter(max_length=4000))
async def handle_text_message(message: Message, session: AsyncSession):
    await message.bot.send_chat_action(message.chat.id, "typing")
    
    user_service = UserService(session)
    user = await user_service.get_user(message.from_user.id)
    
    if not user:
        await message.answer("❌ Ошибка: пользователь не найден. Попробуйте /start")
        return
    
    ai_service = AIService(session)
    response = await ai_service.generate_response(
        user_id=user.id,
        user_message=message.text
    )
    
    if len(response) > 4096:
        for i in range(0, len(response), 4096):
            await message.answer(response[i:i+4096])
    else:
        await message.answer(response)


@router.message(F.text)
async def handle_invalid_message(message: Message):
    if message.text and len(message.text) > 4000:
        await message.answer("❌ Сообщение слишком длинное. Максимум 4000 символов.")
    elif not message.text or not message.text.strip():
        await message.answer("❌ Сообщение не может быть пустым.")