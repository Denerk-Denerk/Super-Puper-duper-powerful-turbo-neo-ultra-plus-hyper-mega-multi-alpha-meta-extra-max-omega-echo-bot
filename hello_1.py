import csv
import asyncio
from aiogram import Bot, Dispatcher, types
import os
from dotenv import load_dotenv

load_dotenv()

def csv_file_open(name_, text):
    with open(name_, 'a', encoding='utf8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow([text])


bot = Bot(token=os.getenv("TOKEN")) # инициализация класса бота
dp = Dispatcher()

@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)
    print(message.text)
    csv_file_open('file.csv', message.text)
     
async def start1():
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(start1())