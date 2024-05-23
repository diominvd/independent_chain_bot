from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils import Translator


def keyboard(event: Message | CallbackQuery, flag: str) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Отмена", callback_data="profile"),
            InlineKeyboardButton(text="Назад", callback_data="profile"),
        ],
        "en": [
            InlineKeyboardButton(text="Cancel", callback_data="profile"),
            InlineKeyboardButton(text="Back", callback_data="profile"),
        ]
    }

    language: str = Translator.language(event)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    if flag == "cancel":
        builder.row(buttons[language][0])
    elif flag == "back":
        builder.row(buttons[language][1])

    return builder.as_markup()