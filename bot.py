from aiogram import Bot, Dispatcher, types, executor
from config import token 
import random

bot = Bot(token=token)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer("Привет! \nУгадай число которое я загадал от 1 до 3")

@dp.message_handler(text=[1,2,3])
async def number(message:types.Message):
    number=random.randint(1,3)
    user = int(message.text)
    if number==user:
        await message.answer('Правильно вы отгадали!')
        await message.answer_photo("https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg")
    else:
        await message.answer('Неправильно вы не отгадали!')
        await message.answer_photo('https://media.makeameme.org/created/sorry-you-lose.jpg')

@dp.message_handler()
async def not_found(message:types.Message):
    await message.reply("Повторите попытку")

executor.start_polling(dp)