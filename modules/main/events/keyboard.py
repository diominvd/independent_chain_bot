from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.config import users_table


def keyboard(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="🎰 Слоты", callback_data="slots"),
            InlineKeyboardButton(text="Назад", callback_data="profile"),
        ],
        "en": [
            InlineKeyboardButton(text="🎰 Slots", callback_data="slots"),
            InlineKeyboardButton(text="Back", callback_data="profile")
        ]
    }

    user_language: str = users_table.get_value("language", "user_id", event.from_user.id)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[user_language][0])
    builder.row(buttons[user_language][1])
    return builder.as_markup()


def keyboard_slots(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Играть", callback_data="spin"),
            InlineKeyboardButton(text="Назад", callback_data="events"),
        ],
        "en": [
            InlineKeyboardButton(text="Play", callback_data="spin"),
            InlineKeyboardButton(text="Back", callback_data="events")
        ]
    }

    user_language: str = users_table.get_value("language", "user_id", event.from_user.id)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[user_language][0])
    builder.row(buttons[user_language][1])
    return builder.as_markup()