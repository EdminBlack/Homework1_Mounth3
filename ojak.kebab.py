from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from logging import basicConfig, INFO
from config import token
from time import ctime
import sqlite3

bot=Bot(token=token)
basicConfig(level=INFO)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
ck=0

database = sqlite3.connect('ojakkebab.db')
cursor = database.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INT,
        username VARCHAR(255),
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        date_joined VARCHAR(255),
        name VARCHAR(255),
        phone INT,
        order_address DOUBLE
    );
""")
cursor.connection.commit()

start_buttons=[
    types.KeyboardButton('/Меню'),
    types.KeyboardButton('/О_нас'),
    types.KeyboardButton('/Адрес'),
    types.KeyboardButton('/Заказать_еду')
]

start_keeyboard=types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    user = cursor.execute(f"SELECT * FROM users WHERE id = {message.from_user.id};")
    result = user.fetchall()
    print(result)
    if result == []:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                       (message.from_user.id, message.from_user.username,
                       message.from_user.first_name, message.from_user.last_name, ctime(), 0, 0, 0))
        cursor.connection.commit()
    await message.answer(f'Здраствуйте,{message.from_user.full_name}!', reply_markup=start_keeyboard)

@dp.message_handler(commands='Меню')
async def menu(message:types.Message):
    await message.answer('https://nambafood.kg/ojak-kebap')

@dp.message_handler(commands='О_нас')
async def about_we(message:types.Message):
    await message.answer('https://ocak.uds.app/c/about')

@dp.message_handler(commands='Адрес')
async def address(message:types.Message):
    await message.answer_location(42.82843201536645, 74.63579318805989)

class MailingState(StatesGroup):
    message= State()

class OrderFoodState(StatesGroup):
    name = State()
    phone = State()
    address = State()

@dp.message_handler(commands='Заказать_еду')
async def order_food(message:types.Message):
    await message.answer('Введите имя')
    await OrderFoodState.name.set()


@dp.message_handler(state=OrderFoodState.name)
async def get_name(message:types.Message , state:FSMContext):
    cursor.execute(f"""UPDATE users SET name = '{message.text}'""")
    cursor.connection.commit()
    await message.answer('Введите номер')
    await OrderFoodState.phone.set() 

@dp.message_handler(state=OrderFoodState.phone)
async def get_phone(message:types.Message , state:FSMContext):
    cursor.execute(f"""UPDATE users SET phone = '{message.text}'""")
    cursor.connection.commit()
    await message.answer('Введите адрес(в координатах)')
    await OrderFoodState.address.set()

@dp.message_handler(state=OrderFoodState.address)
async def get_address(message:types.Message , state:FSMContext):
    cursor.execute(f"""UPDATE users SET order_address = '{message.text}'""")
    cursor.connection.commit()
    await message.answer('Ваши данные сохранены, заказ уже в пути(примерное время:∞)')
    await state.finish()

executor.start_polling(dp)