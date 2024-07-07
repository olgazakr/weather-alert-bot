from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.weather_request import make_request
from app.database.models import async_session, User
from aiogram import Bot
from sqlalchemy import select


async def fetch_and_notify_users(bot: Bot, token: str):
    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
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
                if weather_main in (
                    'Rain', 'Snow', 'Thunderstorm', 'Drizzle', 'Squall', 'Clear',
                    'Mist', 'Haze', 'Fog', 'Dust', 'Smoke', 'Ash', 'Tornado'
                ):

                    message_body = {
                        'weather': weather['weather'][0]['description'],
                        'temp': weather['main']['temp'],
                        'wind': weather['wind']['speed']
                    }
                    message = f'ВНИМАНИЕ!\n{message_body["weather"].title()}\n' \
                              f'Температура: {message_body["temp"]}°C\n' \
                              f'Скорость ветра: {message_body["wind"]} м/с'

                    await bot.send_message(user.telegram_id, message)


def start_scheduler(bot: Bot, token: str):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        fetch_and_notify_users,
        IntervalTrigger(minutes=1),
        args=[bot, token]
    )
    scheduler.start()
