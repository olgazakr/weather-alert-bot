import asyncio
import os
import logging
import location_request

from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message


load_dotenv(find_dotenv())
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Напишите населённый пункт, на который Вы хотите настроить бота.')


@dp.message(F.text)
async def echo(message: Message):
    location = message.text
    possible_locations = location_request.make_request(location, os.getenv('WEATHER_TOKEN'))

    if len(possible_locations) > 1:
        i = 1
        await message.answer(f'Найдено {len(possible_locations)} населённых пунктов. Введите номер одного из них:')
        for location in possible_locations:
            await message.answer(f'{i}. {location["name"]}, {location["state"]}, {location["country"]}')
            i += 1
    elif len(possible_locations) == 1:
        await message.answer(f'Вы выбрали: {possible_locations[0]["name"]}, '
                             f'{possible_locations[0]["country"]}, '
                             f'{possible_locations[0]["state"]}')

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot shutdown.')