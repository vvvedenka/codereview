Telegram Bot: Dictionary Unusual Bot

Dictionary Unusual Bot — это Telegram-бот, который выполняет следующие функции:
/rare_words — редкие слова (длинные слова).
/long_words — длинные слова.
/short_words — короткие слова.
/random_word — случайное слово.

Скрапинг сайта: https://ozhegov.slovaronline.com/ и сохранение их в базу данных PostgreSQL.

Особенности:
автоматизированный запуск, использование Docker, PostgreSQL, aiogram 3x.

Структура:
проект содержит файлы - 
bot.py - основной файл тг-бота,
models.py - определение таблиц бд,
database.py - подключение к бд,
scraper.py - скрипт для парсинга данных,
Dockerfile - для сборки образа,
docker-compose.yml - управление контейнерами docker,
.env - настройки окружения,
requirements.txt - список зависимостей python,
build.sh - скрипт для автоматического запуска проекта.
