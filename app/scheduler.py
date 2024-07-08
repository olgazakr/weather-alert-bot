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
import os

from datetime import datetime
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

                weather_main = weather['weather'][0]['main']
                weather_temp = weather['main']['temp']
                weather_speed = weather['wind']['speed']
                notified_condition = f"{weather_main}-{weather_temp}-{weather_speed}"

                # Check if user was notified
                if user.is_notified:
                    # Notify user if a new 'bad' condition arises
                    if weather_main in (
                        'Rain', 'Snow', 'Thunderstorm', 'Drizzle', 'Squall',
                        'Mist', 'Haze', 'Fog', 'Dust', 'Smoke', 'Ash', 'Tornado'
                    ) or weather_temp > 35 or weather_temp < -15 or weather_speed > 10:
                        if notified_condition != user.notified_condition:
                            user.notified_condition = notified_condition
                            await session.commit()

                            message_body = {
                                'weather': weather['weather'][0]['description'],
                                'temp': weather['main']['temp'],
                                'wind': weather['wind']['speed']
                            }
                            message = f'⚠️ ВНИМАНИЕ! ⚠️\n{message_body["weather"].title()}\n' \
                                    f'Температура: {message_body["temp"]}°C 🌡️\n' \
                                    f'Скорость ветра: {message_body["wind"]} м/с 🌬️'
                            await bot.send_message(user.telegram_id, message)
                else:
                    # Notify user for severe weather conditions
                    if weather_main in (
                        'Rain', 'Snow', 'Thunderstorm', 'Drizzle', 'Squall',
                        'Mist', 'Haze', 'Fog', 'Dust', 'Smoke', 'Ash', 'Tornado'
                    ) or weather_temp > 35 or weather_temp < -15 or weather_speed > 10:
                        user.is_notified = True
                        user.notified_condition = notified_condition
                        await session.commit()

                        message_body = {
                            'weather': weather['weather'][0]['description'],
                            'temp': weather['main']['temp'],
                            'wind': weather['wind']['speed']
                        }
                        message = f'⚠️ ВНИМАНИЕ! ⚠️\n{message_body["weather"].title()}\n' \
                                f'Температура: {message_body["temp"]}°C 🌡️\n' \
                                f'Скорость ветра: {message_body["wind"]} м/с 🌬️'
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
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    # Add a job to the scheduler
    scheduler.add_job(
        fetch_and_notify_users,  # Function to execute
        IntervalTrigger(minutes=1),  # Interval between job executions
        args=[bot, token]  # Arguments to pass to the function
    )
    # Start the scheduler
    scheduler.start()
    # Set up logging
    logger = logging.getLogger('scheduler')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    file_handler = logging.FileHandler(os.path.join('logs', 'scheduler_log.txt'))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info("Scheduler started at %s", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))