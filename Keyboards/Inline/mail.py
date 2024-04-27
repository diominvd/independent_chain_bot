from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def keyboard(language: str) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    names: dict = {
        "ru": ["Перейти на канал"],
        "en": ["Go to the channel"]
    }
    links: dict = {
        "ru": ["https://t.me/inch_ru"],
        "en": ["https://t.me/inch_en"]
    }

    builder.row(
        InlineKeyboardButton(text=names[language][0], url=links[language][0]))
    return builder.as_markup()