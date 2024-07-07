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

                message = f'На данный момент: {weather}'
                await bot.send_message(user.telegram_id, message)


def start_scheduler(bot: Bot, token: str):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        fetch_and_notify_users,
        IntervalTrigger(minutes=1),
        args=[bot, token]
    )
    scheduler.start()
