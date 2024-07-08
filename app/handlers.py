"""
Module that contains the handlers for the bot's commands and states.
"""

import os

import app.database.requests as requests
import app.keyboards as keyboards
import app.weather_request as weather_request
import app.location_request as location_request

from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
router = Router()


class Location(StatesGroup):
    """
    Class that represents the states of the bot.
    """
    input_location = State()
    found_locations = State()
    select_location = State()


@router.message(CommandStart())
async def start_bot(message: Message, state: FSMContext):
    """
    Handler for the /start command.
    Sets the user in the database and starts the bot's state machine.
    """
    telegram_id = message.from_user.id
    telegram_username = message.from_user.username
    await requests.set_user(telegram_id, telegram_username)
    await state.set_state(Location.input_location)
    await message.answer('Напишите населённый пункт,'
                         'на который Вы хотите настроить бота 🌎🌏🌍')
    await state.set_state(Location.found_locations)


@router.message(Location.found_locations)
async def find_locations(message: Message, state: FSMContext):
    """
    Handler for the found_locations state.
    Sends a message with the list of possible locations to select and
    updates the state.
    """
    location = message.text
    possible_locations = await location_request.make_request(
        location,
        os.getenv('WEATHER_TOKEN')
    )
    await state.update_data(found_locations=possible_locations)
    i = 1
    answer = f'Найдено {len(possible_locations)} населённых пунктов 🌇\n' \
              'Выберите один из списка:\n'
    for location in possible_locations:
        answer += f'{i}. {location["name"]}, ' \
                  f'{location["country"]}, ' \
                  f'{location["state"]}\n'
        i += 1
    await message.answer(
        answer,
        reply_markup=await keyboards.get_keyboard(possible_locations)
    )
    await state.set_state(Location.select_location)


@router.callback_query(Location.select_location)
async def select_location(callback: CallbackQuery, state: FSMContext):
    """
    Handler for the select_location state.
    Sets the user's coordinates in the database and sends a message with
    the weather conditions.
    """
    data = await state.get_data()
    answer = data['found_locations'][int(callback.data) - 1]
    await callback.message.edit_text(f'Вы выбрали: {answer["name"]}, '
                                    f'{answer["country"]}, '
                                    f'{answer["state"]}, '
                                    f'координаты: {answer["lat"]}, '
                                    f'{answer["lon"]}'
                                )
    
    await requests.set_coordinates_for_user(
        callback.from_user.id,
        answer['lat'],
        answer['lon']
    )
    
    weather = await weather_request.make_request(
        answer['lat'],
        answer['lon'],
        os.getenv('WEATHER_TOKEN')
    )
    
    if "error" in weather:
        weather_message = "Не удалось получить данные о погоде."
    else:
        weather_message = f'{weather["weather"][0]["description"]}, ' \
                          f'температура: {weather["main"]["temp"]}°C 🌡️, ' \
                          f'скорость ветра: {weather["wind"]["speed"]} м/с 🌬️'

    answer = f'На данный момент: {weather_message}\n' \
              'Бот отслеживает погодные условия в режиме реального времени 🕰️\n' \
              'Он уведомит Вас, если в вашей локации: \n' \
              '1. Температура поднимется выше 35°С или опустится ниже -15°С\n' \
              '2. Скорость ветра превысит 10 м/с\n' \
              '3. Выпадение осадков: дождь 🌧️, снегопад 🌨️, гроза ⛈️\n' \
              '4. Условия ограниченной видимости: туман, мгла 🌫️\n' \
              '5. Экстремальные явления: торнадо 🌪️, выпадение вулканического пепла 🌋'

    await callback.message.answer(answer)

    await state.clear()
