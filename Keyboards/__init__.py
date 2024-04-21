from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from strings import translate_button


def start_keyboard(language: str) -> InlineKeyboardMarkup:
    buttons: list = [
        [InlineKeyboardButton(text=translate_button("main_channel", language), url="https://t.me/inch_coin")],
        [InlineKeyboardButton(text=translate_button("dev_channel", language), url="https://t.me/diominvdev")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard