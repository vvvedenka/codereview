import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from database import SessionLocal
from models import Word
from scraper import fetch_words
from sqlalchemy.sql.expression import func

# Токен Telegram-бота
BOT_TOKEN = os.getenv("7947881343:AAFwarC1O2Mr8nBsGSp50r1VbYyNDJWc9BU")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Команда /start
@dp.message_handler(commands=["start"])
async def start_command(message: Message):
    logging.info(f"Received start command from {message.from_user.id}")
    await message.answer(
        "Привет! Я бот для поиска сложных и редких слов. Выберите команду:\n"
        "/rare_words - редкие слова\n"
        "/long_words - длинные слова\n"
        "/short_words - короткие слова\n"
        "/random_word - случайное слово\n"
    )

# Обработчики команд
@dp.message_handler(commands=["rare_words"])
async def get_rare_words(message: Message):
    session = SessionLocal()
    words = session.query(Word).filter(Word.is_rare == True).limit(10).all()
    session.close()
    word_list = "\n".join([word.text for word in words])
    await message.answer(word_list if word_list else "Редких слов пока нет.")

@dp.message_handler(commands=["long_words"])
async def get_long_words(message: Message):
    session = SessionLocal()
    words = session.query(Word).filter(Word.length > 10).limit(10).all()
    session.close()
    word_list = "\n".join([word.text for word in words])
    await message.answer(word_list if word_list else "Длинных слов пока нет.")

@dp.message_handler(commands=["random_word"])
async def get_random_word(message: Message):
    session = SessionLocal()
    word = session.query(Word).order_by(func.random()).first()
    session.close()
    await message.answer(word.text if word else "Слов пока нет.")

if __name__ == "__main__":
    logging.debug("bot started")
    executor.start_polling(dp, skip_updates=True)
