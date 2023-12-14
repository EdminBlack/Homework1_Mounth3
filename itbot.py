from aiogram import Bot, Dispatcher, types, executor
from logging import basicConfig, INFO
from config import token

bot=Bot(token=token)
dp=Dispatcher(bot)
basicConfig(level=INFO)

start_buttons=[
    types.KeyboardButton('О нас'),
    types.KeyboardButton('Курсы'),
    types.KeyboardButton('Адрес'),
    types.KeyboardButton('Контакты')
]

start_keeyboard=types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f'Здраствуйте,{message.from_user.full_name}!', reply_markup=start_keeyboard)

@dp.message_handler(text='О нас')
async def about_us(message:types.Message):
    await message.reply('Geeks - это айти курсы в Оше, Кара-Балта и БИшкеке основанная в 2019 году')

@dp.message_handler(text='Адрес')
async def send_address(message:types.Message):
    await message.answer('Наш адрес: город Ош, Мырзали Аматова 1Б(БЦ Томирис)')
    await message.answer_location(40.51931846586533, 72.80297788183063)

@dp.message_handler(text='Контакты')
async def send_contacts(message:types.Message):
    await message.answer(f'{message.from_user.full_name} вот наши контакты')
    await message.answer_contact('+996771234213', 'Ulan', 'Ashirov')
    await message.answer_contact('+996777112233', 'Nurbolot', 'Erkinbaev')

courses=[
    types.KeyboardButton('BackEnd'),
    types.KeyboardButton('Frontend'),
    types.KeyboardButton('Android'),
    types.KeyboardButton('IOS'),
    types.KeyboardButton('UX/UI'),
    types.KeyboardButton('Детское програмирование'),
    types.KeyboardButton('Основы програмирования'),
    types.KeyboardButton('Назад')
]

courses_keyboard=types.ReplyKeyboardMarkup(resize_keyboard=True).add(*courses)

@dp.message_handler(text='Курсы')
async def all_courses(message:types.Message):
    await message.answer('Вот наши курсы:', reply_markup=courses_keyboard)

@dp.message_handler(text='BackEnd')

async def backend(message:types.Message):
    await message.answer('Backend - это серверная сторона сайта или приложения. В основном код вам не виден')

@dp.message_handler(text='Frontend')
async def frontend(message:types.Message):
    await message.answer('Frontend - это лицевая часть сайта или приложения. Эту часть вы можете видеть')

@dp.message_handler(text='Android')
async def android(message:types.Message):
    await message.answer('Android - это')

@dp.message_handler(text='IOS')
async def ios(message:types.Message):
    await message.answer('IOS - это')

@dp.message_handler(text='UX/UI')
async def uxui(message:types.Message):
    await message.answer('UX?UI - это дизайн сайта или приложения')

@dp.message_handler(text='Детское програмирование')
async def childrensprogramming(message:types.Message):
    await message.answer('Детское програмирование - это')

@dp.message_handler(text='Основы програмирования')
async def basicprogramming(message:types.Message):
    await message.answer('Основы програмирование - это')

@dp.message_handler(text='Назад')
async def back(message:types.Message):
    await start(message)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_contact(message:types.CallbackQuery):
    await message.answer(message)
    await bot.send_message(-4066726453, f'Заявка на курсы:\n{message.contact}')

executor.start_polling(dp)