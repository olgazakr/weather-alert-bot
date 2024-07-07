import asyncio
import os
import logging

from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.database.models import async_main
from app.scheduler import start_scheduler


async def main():
    await async_main()
    load_dotenv(find_dotenv())
    
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)

    start_scheduler(bot, os.getenv('WEATHER_TOKEN'))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot shutdown.')