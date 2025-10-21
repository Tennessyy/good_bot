#!/usr/bin/env python3
"""
Скрипт для настройки webhook после деплоя на Render
"""
import os
import requests
from config import BOT_TOKEN

def set_webhook(webhook_url):
    """Устанавливает webhook для бота"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    data = {"url": webhook_url}
    
    response = requests.post(url, json=data)
    result = response.json()
    
    if result.get("ok"):
        print(f"✅ Webhook установлен: {webhook_url}")
        print(f"Описание: {result.get('description', '')}")
    else:
        print(f"❌ Ошибка установки webhook: {result}")
    
    return result.get("ok", False)

def get_webhook_info():
    """Получает информацию о текущем webhook"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
    response = requests.get(url)
    result = response.json()
    
    if result.get("ok"):
        webhook_info = result.get("result", {})
        print(f"Текущий webhook: {webhook_info.get('url', 'Не установлен')}")
        print(f"Ожидающие обновления: {webhook_info.get('pending_update_count', 0)}")
    else:
        print(f"❌ Ошибка получения информации: {result}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Использование: python setup_webhook.py <URL_вашего_приложения>")
        print("Пример: python setup_webhook.py https://da-tak-mozhno-bot.onrender.com/webhook")
        sys.exit(1)
    
    webhook_url = sys.argv[1]
    
    print("🔍 Проверяем текущий webhook...")
    get_webhook_info()
    
    print(f"\n🔧 Устанавливаем webhook: {webhook_url}")
    success = set_webhook(webhook_url)
    
    if success:
        print("\n🎉 Готово! Бот теперь работает через webhook.")
    else:
        print("\n❌ Не удалось установить webhook. Проверьте URL и токен.")