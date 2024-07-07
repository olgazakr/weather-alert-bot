"""
Fetch and notify users of severe weather conditions.
This function fetches weather data for all users with coordinates and notifies them
if severe weather conditions are detected. It uses the :class:`Bot` class from
`aiogram` to send messages to users.

:param bot: An instance of the :class:`Bot` class from `aiogram`.
:type bot: aiogram.Bot
:param token: The API token for the OpenWeatherMap API.
:type token: str
"""
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.weather_request import make_request
from app.database.models import async_session, User
from aiogram import Bot
from sqlalchemy import select

async def fetch_and_notify_users(bot: Bot, token: str):
    """
    Fetch weather data for all users with coordinates and notify them if
    severe weather conditions are detected.

    :param bot: An instance of the :class:`Bot` class from `aiogram`.
    :type bot: aiogram.Bot
    :param token: The API token for the OpenWeatherMap API.
    :type token: str
    """
    async with async_session() as session:
        # Fetch all users with coordinates from the database
        result = await session.execute(select(User))
        users = result.scalars().all()

        # Iterate over each user and check for severe weather conditions
        for user in users:
            if user.latitude and user.longitude:
                weather = await make_request(
                    user.latitude,
                    user.longitude,
                    token
                )
                if 'error' in weather:
                    continue

                weather_main = weather['weather'][0]['main']
                weather_temp = weather['main']['temp']
                weather_speed = weather['wind']['speed']
                # Check for severe weather conditions
                if weather_main in (
                    'Rain', 'Snow', 'Thunderstorm', 'Drizzle', 'Squall',
                    'Mist', 'Haze', 'Fog', 'Dust', 'Smoke', 'Ash', 'Tornado'
                ) or weather_temp > 35 or weather_temp < -15 or weather_speed > 10:
                    # Build message body
                    message_body = {
                        'weather': weather['weather'][0]['description'],
                        'temp': weather['main']['temp'],
                        'wind': weather['wind']['speed']
                    }
                    # Build message
                    message = f'ВНИМАНИЕ!\n{message_body["weather"].title()}\n' \
                              f'Температура: {message_body["temp"]}°C\n' \
                              f'Скорость ветра: {message_body["wind"]} м/с'
                    # Send message to user
                    await bot.send_message(user.telegram_id, message)


def start_scheduler(bot: Bot, token: str):
    """
    Starts an asynchronous scheduler that fetches weather data for all users
    with coordinates and notifies them if severe weather conditions are
    detected. The scheduler runs every minute.

    :param bot: An instance of the :class:`Bot` class from `aiogram`.
    :type bot: aiogram.Bot
    :param token: The API token for the OpenWeatherMap API.
    :type token: str
    """
    # Create an asynchronous scheduler
    scheduler = AsyncIOScheduler()

    # Add a job to the scheduler
    scheduler.add_job(
        fetch_and_notify_users,  # Function to execute
        IntervalTrigger(minutes=1),  # Interval between job executions
        args=[bot, token]  # Arguments to pass to the function
    )

    # Start the scheduler
    scheduler.start()
