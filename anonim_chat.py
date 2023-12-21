from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from tokens import token 
import sqlite3


bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

connection = sqlite3.connect('bank_bot.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username VARCHAR(255),
        first_name VARCHAR(255),
        last_name VARCHAR(255)
    )
''')
connection.commit()

@dp.message_handler(commands='start')
async def start(message:types.Message):
    user = cursor.execute(f"SELECT * FROM users WHERE id = {message.from_user.id};")
    result = user.fetchall()
    print(result)
    if result == []:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", 
                       (message.from_user.id, message.from_user.username,
                       message.from_user.first_name, message.from_user.last_name))
        cursor.connection.commit()
    await message.answer(f'Вы были зарегестриррованы в базу данных')


