from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def get_keyboard(possible_locations: list) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    i = 1
    for location in possible_locations:
        keyboard.add(
            InlineKeyboardButton(
                text=f'{i}', callback_data=f'{i}'
            )
        )
        i += 1

    return keyboard.as_markup()