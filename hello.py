
import asyncio
import csv
import os

from aiogram.filters import Command, CommandObject
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()


def write_to_csv_file(name, text, user_name, user_id, date):
    with open(name, 'a', encoding='utf8', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow([user_name, date, text, user_id])

        
def reader_to_csv_file(name_csv):
    with open(name_csv, newline='', encoding='utf-8', mode='r') as f:
        reader = csv.reader(f, delimiter=';')
        return [row for row in reader][::-1]


def create_format(row):
    return f"{row[0]} | {row[1]} | {row[2]}"

bot = Bot(token=os.getenv("TOKEN"), encode='utf-8')
dp = Dispatcher()

@dp.message(Command('history'))
async def history(message: types.Message, command: CommandObject):
    history = reader_to_csv_file('file.csv')
    length = command.args
    counter = int(length) if length else 10
    id_us = str(message.from_user.id)
    text = []
    for row in history:
        if row[3] == id_us:
            counter -= 1
            text.append(create_format(row))
        if counter <= 0:
            break
    await message.answer('\n'.join(text))

@dp.message(Command('stats'))
async def stats(message: types.Message):
    history = reader_to_csv_file('file.csv')
    users = {}
    text = []
    for row in history:
        if row[0] not in users:
            users.update({row[0]:0})
        users[row[0]]+=1
    for user in users:
        text.append(f"{user}: {users[user]}")
    await message.answer('\n'.join(text))
        


@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)
    write_to_csv_file('file.csv', message.text, message.from_user.first_name, message.from_user.id, datetime.strptime(str(message.date.astimezone()), "%Y-%m-%d %H:%M:%S%z").strftime("%Y-%m-%d %H:%M:%S"))

async def start():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start())