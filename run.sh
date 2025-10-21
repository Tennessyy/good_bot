#!/bin/bash

# Скрипт для запуска бота "Да, так можно"

echo "🚀 Запуск бота 'Да, так можно'..."

# Проверяем наличие Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Пожалуйста, установите Docker"
    exit 1
fi

# Проверяем наличие docker-compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Пожалуйста, установите Docker Compose"
    exit 1
fi

# Создаем директорию для логов
mkdir -p logs

# Останавливаем предыдущие контейнеры (если есть)
echo "🛑 Останавливаем предыдущие контейнеры..."
docker-compose down

# Собираем и запускаем
echo "🔨 Собираем и запускаем бота..."
docker-compose up --build -d

# Проверяем статус
sleep 5
if docker-compose ps | grep -q "Up"; then
    echo "✅ Бот успешно запущен!"
    echo "📋 Для просмотра логов: docker-compose logs -f"
    echo "🛑 Для остановки: docker-compose down"
else
    echo "❌ Ошибка при запуске. Проверьте логи: docker-compose logs"
fi 