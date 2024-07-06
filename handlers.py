import location_request
import os

from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import F, Router
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer('Напишите населённый пункт, на который Вы хотите настроить бота.')


@router.message(F.text)
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