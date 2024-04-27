from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def keyboard(language: str) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    names: dict = {
        "ru": ["Назад"],
        "en": ["Back"]
    }

    builder.row(
        InlineKeyboardButton(text=names[language][0], callback_data="profile"))
    return builder.as_markup()