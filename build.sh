#!/bin/bash
export $(grep -v '^#' .env | xargs)
echo "Собираем и запускаем проект через Docker Compose..."
docker-compose down --volumes
docker-compose up --build -d
echo "Ожидаем запуска PostgreSQL..."
until docker exec telegram_bot_db pg_isready -U vvvedenka > /dev/null 2>&1; do
  echo "PostgreSQL ещё не готов, подождите 5 секунд..."
  sleep 5
done
echo "PostgreSQL готов. Выполняем скрапинг данных..."
docker exec -it dictionary_unusual_bot  python3 /app/scraper.py
echo "Проект запущен. Telegram-бот работает!"
