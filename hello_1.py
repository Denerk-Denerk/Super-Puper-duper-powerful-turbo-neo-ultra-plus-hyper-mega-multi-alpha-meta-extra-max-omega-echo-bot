import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message



bot = Bot(token='7963317130:AAEfdEY08QA4CF-2mJO3OPQ3UqQ2iXDzr_8')
dp = Dispatcher()

@dp.message()
async def smd_start(message: Message):
    await message.answer(message.text)
     
async def start1():
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(start1())