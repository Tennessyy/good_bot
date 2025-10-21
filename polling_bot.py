#!/usr/bin/env python3
"""
Простой polling бот для Render
"""
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    CallbackQueryHandler,
    filters, 
    ContextTypes
)
from config import BOT_TOKEN, CHANNEL_ID, WELCOME_MESSAGE, HELP_MESSAGE

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Словарь для хранения историй пользователей
user_stories = {}

def extract_urls(text):
    """Извлекает URL из текста"""
    import re
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.findall(url_pattern, text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text(WELCOME_MESSAGE)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    await update.message.reply_text(HELP_MESSAGE)

async def handle_story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик историй от пользователей"""
    user = update.message.from_user
    message_text = update.message.text
    
    # Проверяем минимальную длину сообщения
    if len(message_text.split()) < 5:
        await update.message.reply_text(
            "Пожалуйста, отправь более подробное сообщение о том, что тебя вдохновляет! 🙂"
        )
        return
    
    # Сохраняем историю пользователя временно
    user_stories[user.id] = message_text
    
    # Создаем клавиатуру с выбором способа публикации
    keyboard = [
        [
            InlineKeyboardButton("👤 С указанием профиля", callback_data=f"with_profile_{user.id}"),
            InlineKeyboardButton("🕶 Анонимно", callback_data=f"anonymous_{user.id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Спрашиваем у пользователя способ публикации
    await update.message.reply_text(
        "📝 Твоя история готова к публикации!\n\n"
        "Опубликовать анонимно или с указанием профиля?",
        reply_markup=reply_markup
    )

async def handle_publication_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик выбора способа публикации"""
    query = update.callback_query
    await query.answer()
    
    # Парсим данные из callback
    callback_data = query.data
    if callback_data.startswith("with_profile_"):
        user_id = int(callback_data.replace("with_profile_", ""))
        is_anonymous = False
    elif callback_data.startswith("anonymous_"):
        user_id = int(callback_data.replace("anonymous_", ""))
        is_anonymous = True
    else:
        await query.edit_message_text("❌ Ошибка обработки запроса.")
        return
    
    # Получаем сохраненную историю
    if user_id not in user_stories:
        await query.edit_message_text("❌ История не найдена. Попробуй отправить её заново.")
        return
    
    message_text = user_stories[user_id]
    user = query.from_user
    
    # Формируем сообщение для канала
    if is_anonymous:
        channel_message = f"{message_text}\n\n🕯️ Анонимная история"
    else:
        channel_message = f"{message_text}\n\n🕯️ История от @{user.username or user.first_name}"
    
    try:
        # Отправляем в канал
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=channel_message,
            disable_web_page_preview=False
        )
        
        # Подтверждение пользователю
        publication_type = "анонимно" if is_anonymous else "с указанием профиля"
        await query.edit_message_text(
            f"✅ Спасибо! Твоя история опубликована в канале 'Да, так реально' {publication_type}!\n\n"
            "Продолжай делиться вдохновляющими историями! 🌟"
        )
        
        logger.info(f"Story posted from user {user.username or user.first_name} ({user.id}), anonymous: {is_anonymous}")
        
        # Удаляем историю из временного хранилища
        del user_stories[user_id]
        
    except Exception as e:
        logger.error(f"Error posting to channel: {e}")
        await query.edit_message_text(
            "😔 Произошла ошибка при публикации. Попробуй еще раз или обратись к администратору."
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Главная функция - запуск бота"""
    try:
        # Создаем приложение
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Регистрируем обработчики
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CallbackQueryHandler(handle_publication_choice))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_story))
        
        # Обработчик ошибок
        application.add_error_handler(error_handler)
        
        # Запускаем бота
        logger.info("Бот запущен!")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")

if __name__ == '__main__':
    main()