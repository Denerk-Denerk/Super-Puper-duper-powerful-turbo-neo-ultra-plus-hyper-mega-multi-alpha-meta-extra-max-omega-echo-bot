
import asyncio

from aiogram.filters import Command, CommandObject
from aiogram import Bot, Dispatcher, types
from datetime import datetime

import settings
from utils import reader_to_csv_file, write_to_csv_file, create_format, write_to_csv_stat


bot = Bot(token=settings.TOKEN, encode='utf-8')

dp = Dispatcher()


@dp.message(Command('history'))
async def history(message: types.Message, command: CommandObject):
    history = reader_to_csv_file('file.csv')
    length = command.args
    counter = int(length) if length else 10
    id_us = str(message.from_user.id)
    text = []
    for row in history:
        if row['user_id'] == id_us:
            counter -= 1
            text.append(create_format(row))
        if counter <= 0:
            break
    await message.answer('\n'.join(text))


@dp.message(Command('stats'))
async def stats(message: types.Message, command: CommandObject):
    history = reader_to_csv_file('file.csv')
    stats = reader_to_csv_file('stats.csv')
    length = command.args
    users = {}
    text = []
    if length:
        date_all = length.split(' ')
        date_start = datetime.strptime(' '.join(date_all[:2]), '%Y-%m-%d %H:%M:%S')  
        date_end = datetime.strptime(' '.join(date_all[2:]), '%Y-%m-%d %H:%M:%S')
        if date_start >= date_end:
            await message.answer("Некорректный ввод даты")
        else:
            for row in history:
                date_row = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
                if date_start <= date_row <= date_end:
                    if row[0] not in users:
                        users.update({row[0]: 0})
                    users[row[0]] += 1
            for user in users:
                text.append(f"{user}: {users[user]}")
            await message.answer('\n'.join(text) if text else "Нет сообщений за этот период")
            
    else:
        text = []
        last_id_user = history[0]['message_id']
        for user in stats:
            last_id = user['last_message_id']
            if last_id_user == last_id:
                for user in stats:
                    text.append(f"{user['username']}: {user['stat']}\n")
                await message.answer(''.join(text))
        if not text:
            for row in history:
                if row['username'] not in users:
                    users.update({row['username']: 0})
                users[row['username']] += 1
            for user in users:
                text.append(f"{user}: {users[user]}")
            await message.answer('\n'.join(text))
            text.clear()
            for user in users:
                for row in history:
                    if row['username'] == user:
                        text.append([user, str(users[user]), row['message_id']])
                        break
                    
            write_to_csv_stat('stats.csv', text)
                
        


@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)
    write_to_csv_file(
        'file.csv',
        message.text,
        message.from_user.first_name,
        message.from_user.id,
        datetime.strptime(
            str(message.date.astimezone()),"%Y-%m-%d %H:%M:%S%z").strftime("%Y-%m-%d %H:%M:%S"),
        message.message_id
    )


async def start():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start())