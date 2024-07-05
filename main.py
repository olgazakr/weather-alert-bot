import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Напишите населённый пункт, на который Вы хотите настроить бота.')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())