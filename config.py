# БИБЛИОТЕКА ИМПОРТОВ
import os
import sqlite3

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode

from aiogram.contrib.fsm_storage.memory import MemoryStorage


load_dotenv()


# ОБЪЯВЛЕНИЕ ЭКЗЕМПЛЯРОВ

BOT_TOKEN = os.getenv('BOT_TOKEN')

DEVELOPER = int(os.getenv('developer'))
OWNER = int(os.getenv('owner'))

dev_list = [DEVELOPER, OWNER]


bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

db = sqlite3.connect('database.db')