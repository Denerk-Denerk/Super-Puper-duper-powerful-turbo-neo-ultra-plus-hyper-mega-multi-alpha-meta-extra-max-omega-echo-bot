import asyncio
import csv
import os

from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv


load_dotenv()


def write_to_csv_file(name, text):
    with open(name, 'a', encoding='utf8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow([text])


bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()


@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)
    write_to_csv_file('file.csv', message.text)


async def start():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start())
