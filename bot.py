import os
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton
from database import SessionLocal
from models import Word
from scraper import fetch_words
from sqlalchemy.sql.expression import func
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

# Логирование
logging.basicConfig(level=logging.INFO)

# Токен Telegram-бота
BOT_TOKEN = os.getenv("7947881343:AAFwarC1O2Mr8nBsGSp50r1VbYyNDJWc9BU")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Команда /start
@dp.message(Command("start"))
async def start_command(message: Message):
    logging.info(f"Received start command from {message.from_user.id}")
    await message.answer(
        "Привет! Я бот для поиска сложных и редких слов. Выберите команду:\n"
        "/rare_words - редкие слова\n"
        "/long_words - длинные слова\n"
        "/short_words - короткие слова\n"
        "/random_word - случайное слово\n"
    )

# Команда /rare_words
@dp.message(Command("rare_words"))
async def get_rare_words(message: Message):
    session = SessionLocal()
    words = session.query(Word).filter(Word.is_rare == True).limit(10).all()
    session.close()
    word_list = "\n".join([word.text for word in words])
    await message.answer(word_list if word_list else "Редких слов пока нет.")

# Команда /long_words
@dp.message(Command("long_words"))
async def get_long_words(message: Message):
    session = SessionLocal()
    words = session.query(Word).filter(Word.length > 10).limit(10).all()
    session.close()
    word_list = "\n".join([word.text for word in words])
    await message.answer(word_list if word_list else "Длинных слов пока нет.")

# Команда /random_word
@dp.message(Command("random_word"))
async def get_random_word(message: Message):
    session = SessionLocal()
    word = session.query(Word).order_by(func.random()).first()
    session.close()
    await message.answer(word.text if word else "Слов пока нет.")

# Главная точка запуска
async def main():
    logging.info("Starting bot")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
