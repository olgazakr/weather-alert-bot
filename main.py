import asyncio
import os
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Напишите населённый пункт, на который Вы хотите настроить бота.')


@dp.message(F.text)
async def echo(message: Message):
    await message.answer('Населённый пункт установлен. Ожидайте ответа.')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot shutdown.')