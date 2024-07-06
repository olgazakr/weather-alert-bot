import location_request
import os
import keyboards

from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer('Напишите населённый пункт, на который Вы хотите настроить бота.')


@router.message(F.text)
async def select_location(message: Message):
    location = message.text
    possible_locations = location_request.make_request(location, os.getenv('WEATHER_TOKEN'))

    if len(possible_locations) > 1:
        i = 1
        answer = f'Найдено {len(possible_locations)} населённых пунктов. Выберите один из списка:\n'
        for location in possible_locations:
            answer += f'{i}. {location["name"]}, {location["country"]}, {location["state"]}\n'
            i += 1
        await message.answer(answer, reply_markup=await keyboards.get_keyboard(possible_locations))
    elif len(possible_locations) == 1:
        await message.answer(f'Вы выбрали: {possible_locations[0]["name"]}, '
                             f'{possible_locations[0]["country"]}, '
                             f'{possible_locations[0]["state"]}')