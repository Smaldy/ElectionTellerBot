import pandas as pd
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bot = Bot(token='6282517420:AAEkxEga1MAlR7W2Sp1JnESO1SrUTGs2A6k')
dp = Dispatcher(bot)
button1 = KeyboardButton('Hello!')
button2 = KeyboardButton('Youtube')
keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button1, button2)

@dp.message_handler()
async def handle_messages(message: types.Message):
    if message.text == 'Hello!':
        await message.answer('Risposta al pulsante "Hello!"')
    elif message.text == 'Youtube':
        await message.answer('Risposta al pulsante "Youtube"')

    await message.answer("yo", reply_markup=keyboard1)


executor.start_polling(dp)
