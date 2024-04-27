from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def keyboard(language: str) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    names: dict = {
        "ru": ["Канал проекта", "Проверить ✅"],
        "en": ["Project channel", "Check ✅"]
    }
    links: dict = {
        "ru": ["https://t.me/inch_ru"],
        "en": ["https://t.me/inch_en"]
    }

    builder.row(
        InlineKeyboardButton(text=names[language][0], url=links[language][0]))
    builder.row(
        InlineKeyboardButton(text=names[language][1], callback_data="check_subscribe"))
    return builder.as_markup()