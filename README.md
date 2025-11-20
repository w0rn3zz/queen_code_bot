# Queen Code Bot

AI-ассистент бот для Telegram с функциями модерации контента и административной панелью.

## Возможности

- 🤖 AI-ассистент на базе GigaChat
- 🛡️ Фильтрация контента и банвордов
- 👥 Система администрирования
- 📊 Хранение истории сообщений
- 🚫 Защита от спама и флуда

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/w0rn3zz/queen_code_bot.git
cd queen_code_bot
```

2. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

3. Заполните `.env` файл:
```env
BOT_TOKEN=ваш_токен_бота
ADMIN_ID=ваш_telegram_id
GIGACHAT_API_KEY=ваш_api_ключ
```

4. Соберите и запустите через Docker:
```bash
docker-compose up --build -d
```

Миграции применятся автоматически при запуске.

## Админская панель

### Команды управления банвордами

- `/admin` - Открыть панель администратора
- `/banwords_list` - Показать все банворды
- `/add_banword <слово>` - Добавить одно слово
- `/add_banwords <слова>` - Добавить несколько слов (через пробел/запятую)
- `/remove_banword <слово>` - Деактивировать слово
- `/delete_banword <слово>` - Удалить слово полностью

### Загрузка банвордов из файла

Отправьте `.txt` файл с банвордами (каждое слово с новой строки), и бот автоматически добавит их в базу.

### Команды управления администраторами

- `/admins_list` - Список всех администраторов
- `/add_admin <telegram_id>` - Добавить администратора
- `/remove_admin <telegram_id>` - Удалить администратора

Главный администратор (указанный в `ADMIN_ID`) не может быть удален.

## Тестирование

Проект включает набор unit-тестов для проверки функциональности хэндлеров бота.

### Установка зависимостей для тестов

```bash
uv sync
```

### Запуск тестов

Запустить все тесты:
```bash
uv run pytest
```

Запустить с подробным выводом:
```bash
uv run pytest -v
```

Запустить конкретный файл тестов:
```bash
uv run pytest tests/test_admin_handlers.py
uv run pytest tests/test_user_handlers.py

### Структура тестов

- `tests/test_admin_handlers.py` - Тесты административных команд (18 тестов)
- `tests/test_user_handlers.py` - Тесты пользовательских команд (12 тестов)
- `tests/conftest.py` - Фикстуры и настройки для тестов

Все тесты используют моки для изоляции и не требуют реальной БД или API ключей.

## Структура проекта

```
queen_code_bot/
├── docker/
│   ├── scripts/          # Скрипты для Docker
│   │   └── entrypoint.sh # Автозапуск миграций
│   └── volumes/          # Volumes для данных
│       ├── postgres/
│       └── redis/
├── src/
│   ├── bot/
│   │   ├── handlers/     # Обработчики команд
│   │   │   ├── user.py   # Пользовательские команды
│   │   │   └── admin.py  # Админские команды
│   │   └── filters/      # Фильтры сообщений
│   ├── core/
│   │   ├── config/       # Конфигурация
│   │   └── models/       # Модели БД
│   ├── dao/              # Data Access Objects
│   ├── services/         # Бизнес-логика
│   └── middlewares/      # Middleware
├── alembic/              # Миграции БД
└── docker-compose.yml
```

## Технологии

- Python 3.11+
- aiogram 3.x
- SQLAlchemy 2.x
- PostgreSQL
- Redis
- GigaChat API
- Docker
