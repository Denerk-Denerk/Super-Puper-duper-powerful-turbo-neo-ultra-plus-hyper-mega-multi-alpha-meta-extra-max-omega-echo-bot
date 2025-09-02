
import asyncio
from collections import defaultdict

from aiogram.filters import Command, CommandObject
from aiogram import Bot, Dispatcher, types
from datetime import datetime

import settings
from utils import (
    date_range_format,
    filter_msgs_by_user_id,
    read_csv_file,
    write_to_csv_file
)


bot = Bot(token=settings.TOKEN, encode='utf-8')

dp = Dispatcher()


@dp.message(Command('history'))
async def history(message: types.Message, command: CommandObject):
    history = read_csv_file(fname='history.csv', fields=["date", "user_id", "user_name", "text"])
    length = command.args
    counter = int(length) if length else 10
    user_id = str(message.from_user.id)
    text = []

    user_messages = filter_msgs_by_user_id(history, user_id, counter)
    text = [row for row in user_messages]

    msg = '\n'.join(text) if text else "No history for you"
    await message.answer(text=msg)


@dp.message(Command('stats'))
async def stats(message: types.Message, command: CommandObject):
    history = read_csv_file(fname='history.csv', fields=["date", "user_id", "user_name", "text"])
    args = command.args
    users = defaultdict(int)
    text = []

    start, end = date_range_format(args)
    for row in history:
        date_field = datetime.strptime(row["date"], '%Y-%m-%d %H:%M:%S')
        if start <= date_field <= end:
            users[row["user_name"]] += 1

    for user in users:
        text.append(f"{user}: {users[user]}")

    msg = '\n'.join(text) if text else "Нет сообщений за этот период"
    await message.answer(msg)


@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)
    data = {
        "date": message.date.astimezone().strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": message.from_user.id,
        "user_name": message.from_user.first_name,
        "text": message.text,

    }
    write_to_csv_file(fname='history.csv', data=data)
    # UPDATE STATS HERE


async def start():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start())
