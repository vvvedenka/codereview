# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Создаём рабочую директорию
WORKDIR /app

# Копируем зависимости Python (т.е. requirements.txt)
COPY requirements.txt ./

# Устанавливаем Python-зависимости
RUN pip3 install -r requirements.txt

# Копируем исходный код
COPY scraper.py /app/scraper.py

# Запускаем Telegram-бота
CMD ["python3", "bot.py"]
