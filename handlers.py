import location_request
import os
import keyboards

from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
router = Router()

class Location(StatesGroup):
    input_location = State()
    found_locations = State()
    select_location = State()


@router.message(CommandStart())
async def start_bot(message: Message, state: FSMContext):
    await state.set_state(Location.input_location)
    await message.answer('Напишите населённый пункт, на который Вы хотите настроить бота.')
    await state.set_state(Location.found_locations)


@router.message(Location.found_locations)
async def find_locations(message: Message, state: FSMContext):
    location = message.text
    possible_locations = location_request.make_request(location, os.getenv('WEATHER_TOKEN'))
    await state.update_data(found_locations=possible_locations)
    i = 1
    answer = f'Найдено {len(possible_locations)} населённых пунктов. Выберите один из списка:\n'
    for location in possible_locations:
        answer += f'{i}. {location["name"]}, {location["country"]}, {location["state"]}\n'
        i += 1
    await message.answer(answer, reply_markup=await keyboards.get_keyboard(possible_locations))
    await state.set_state(Location.select_location)


@router.callback_query(Location.select_location)
async def select_location(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    answer = data['found_locations'][int(callback.data) - 1]
    await callback.message.answer(f'Вы выбрали: {answer["name"]}, '
                                  f'{answer["country"]}, '
                                  f'{answer["state"]}, '
                                  f'координаты: {answer["lat"]}, '
                                  f'{answer["lon"]}')
    await state.clear()