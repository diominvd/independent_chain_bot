from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.config import users_table


def keyboard_cancel(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Отмена", callback_data="profile")
        ],
        "en": [
            InlineKeyboardButton(text="Cancel", callback_data="profile")
        ]
    }

    user_language: str = users_table.get_value("language", "user_id", event.from_user.id)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[user_language][0])
    return builder.as_markup()


def keyboard_finish(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Закрыть", callback_data="profile")
        ],
        "en": [
            InlineKeyboardButton(text="Close", callback_data="profile")
        ]
    }

    user_language: str = users_table.get_value("language", "user_id", event.from_user.id)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[user_language][0])
    return builder.as_markup()