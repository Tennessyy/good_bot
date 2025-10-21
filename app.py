import logging
import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
import asyncio
from config import BOT_TOKEN, CHANNEL_ID, WELCOME_MESSAGE, HELP_MESSAGE
from bot import (
    start, help_command, handle_story, handle_publication_choice, 
    error_handler, user_stories
)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Глобальная переменная для приложения бота
bot_application = None

async def create_bot_app():
    """Создает приложение бота для webhook"""
    global bot_application
    if bot_application is None:
        bot_application = Application.builder().token(BOT_TOKEN).build()
        
        # Регистрируем обработчики
        bot_application.add_handler(CommandHandler("start", start))
        bot_application.add_handler(CommandHandler("help", help_command))
        bot_application.add_handler(CallbackQueryHandler(handle_publication_choice))
        bot_application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_story))
        
        # Обработчик ошибок
        bot_application.add_error_handler(error_handler)
        
        # Инициализируем приложение
        await bot_application.initialize()
        await bot_application.start()
        
        logger.info("Bot application initialized for webhook")

@app.on_event("startup")
async def startup_event():
    """Инициализация при запуске"""
    await create_bot_app()

@app.on_event("shutdown")
async def shutdown_event():
    """Очистка при остановке"""
    global bot_application
    if bot_application:
        await bot_application.stop()
        await bot_application.shutdown()

@app.post("/webhook")
async def webhook(request: Request):
    """Обработчик webhook от Telegram"""
    try:
        data = await request.json()
        update = Update.de_json(data, bot_application.bot)
        
        if update:
            await bot_application.process_update(update)
            return {"status": "ok"}
        else:
            logger.warning("Received empty update")
            return {"status": "error", "message": "Empty update"}
            
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/")
async def root():
    """Корневой эндпоинт для проверки"""
    return {"status": "Bot is running", "service": "da-tak-mozhno-bot"}

@app.get("/health")
async def health():
    """Health check для мониторинга"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)