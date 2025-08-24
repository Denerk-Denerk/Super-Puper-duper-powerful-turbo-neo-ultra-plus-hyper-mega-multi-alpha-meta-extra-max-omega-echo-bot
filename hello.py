
import asyncio
import csv
import os

from aiogram.filters import Command, CommandObject
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv


load_dotenv()


def write_to_csv_file(name, text):
    with open(name, 'a', encoding='utf8', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow([text])

        
def csv_file_reader(name_csv):
    with open(name_csv, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        return [row for row in reader]


bot = Bot(token=os.getenv("TOKEN"), encode='utf-8')
dp = Dispatcher()

@dp.message(Command('history'))
async def history(message: types.Message, command: CommandObject):
    history = csv_file_reader('file.csv')
    length = command.args
    if length:
        await message.answer('\n'.join([row[0] for row in history[:int(length)] if row]))
    else:
        await message.answer('\n'.join([row[0] for row in history if row]))



@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)
    write_to_csv_file('file.csv', message.text)
    

async def start():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start())