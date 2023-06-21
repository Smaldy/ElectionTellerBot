import csv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bot = Bot(token='6265945877:AAGeiaPR9mmYXT_6xCGo-gN5fGGyUqBuXAI')
dp = Dispatcher(bot)
button1 = KeyboardButton('Hello!')
button2 = KeyboardButton('Youtube')
button3 = KeyboardButton('prova')
keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button1, button2,button3)

@dp.message_handler()
async def handle_messages(message: types.Message):
    if message.text == 'Hello!':
        await message.answer('Risposta al pulsante "Hello!"')
    elif message.text == 'Youtube':
        await message.answer('Risposta al pulsante "Youtube"')
    elif message.text == 'prova':
        with open('Elezioni_Villafranca.csv', 'r') as file:
            reader = csv.reader(file)
            first_row = next(reader)
            lista = []
            indice = [1,3,5];
        for item in first_row:
            lista.extend(item.split(';'))
        listaSindaci = []
        for i in indice:
            listaSindaci.append(lista[i])
            print(lista)
    await message.answer("yo", reply_markup=keyboard1)


executor.start_polling(dp)