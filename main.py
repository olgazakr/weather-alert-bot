"""
Main module that starts the bot.

This module is responsible for initializing the bot and starting the scheduler.

The bot is initialized with the token stored in the environment variable `TOKEN`.
The scheduler is started with the weather token stored in the environment variable `WEATHER_TOKEN`.

The bot is started with the `start_polling` method of the `aiogram.Dispatcher` class.

The bot uses the `app.handlers.router` to handle incoming messages.

The database is initialized using the `app.database.models.async_main` function.

The `async_main` function is called before initializing the bot to ensure that the database is properly set up.

The `start_scheduler` function is called to start the scheduler. This function is defined in the `app.scheduler` module.

The bot uses the `logging` module to log information at the INFO level.

The bot is shut down gracefully when the program is interrupted with a keyboard interrupt or system exit.

"""

import asyncio
import os
import logging

from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.database.models import async_main
from app.scheduler import start_scheduler


async def main():
    """
    Initialize the bot and start the scheduler.

    This function is called when the program is run.
    It initializes the bot and starts the scheduler.

    """
    # Initialize the database
    await async_main()

    # Load environment variables
    load_dotenv(find_dotenv())

    # Create a bot instance with the token from the environment variable
    bot = Bot(token=os.getenv('TOKEN'))

    # Create a dispatcher instance and include the router
    dp = Dispatcher()
    dp.include_router(router)

    # Start the scheduler with the weather token from the environment variable
    start_scheduler(bot, os.getenv('WEATHER_TOKEN'))

    # Start polling for incoming messages
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Configure logging at the INFO level
    logging.basicConfig(level=logging.INFO)

    try:
        # Run the main function with asyncio
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        # Print a message when the bot is shut down gracefully
        print('Bot shutdown.')