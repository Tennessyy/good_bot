import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

"""Configuration module for environment-based settings.

BOT_TOKEN must be provided via environment; no insecure default is kept.
"""

# Настройки бота
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set. Provide it via environment variable BOT_TOKEN")

CHANNEL_ID = os.getenv('CHANNEL_ID', '@da_tak_realno')

# Приветственное сообщение
WELCOME_MESSAGE = """Привет, это бот для историй "Да, так можно"

Чтобы поделиться своей историей, которая тебя вдохновляет, отправь:
📰 Ссылку на новость + комментарий, почему она вдохновила
👤 Ссылку на личную страницу человека + описание его поступка
✨ Или просто свою личную вдохновляющую историю

После отправки истории ты сможешь выбрать способ публикации:
🕶 Анонимно (без указания твоего профиля)
👤 С указанием профиля

Твоя история опубликуется в канале "Да, так реально" ✨"""

# Команды
HELP_MESSAGE = """
Доступные команды:
/start - Запустить бота
/help - Показать это сообщение

Просто отправь сообщение с ссылкой и комментарием, чтобы поделиться историей!
""" 