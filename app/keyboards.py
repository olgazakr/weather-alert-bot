"""
This module contains functions for creating inline keyboards with callback data.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def get_keyboard(possible_locations: list) -> InlineKeyboardMarkup:
    """
    This function creates an inline keyboard with callback data for each possible location.

    :param possible_locations: A list of dictionaries containing information about possible locations.
    :type possible_locations: list
    :return: An instance of the InlineKeyboardMarkup class.
    :rtype: InlineKeyboardMarkup
    """
    keyboard = InlineKeyboardBuilder()
    i = 1
    for location in possible_locations:
        # Add a button to the keyboard with the index of the location as the callback data
        keyboard.add(
            InlineKeyboardButton(
                text=f'{i}',  # Display the index of the location on the button
                callback_data=f'{i}'  # Use the index as the callback data
            )
        )
        i += 1

    return keyboard.as_markup()
