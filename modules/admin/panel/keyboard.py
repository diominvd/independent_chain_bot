from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.config import users_table


def keyboard(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Сообщения", callback_data="messages"),
            InlineKeyboardButton(text="База данных", callback_data="database"),
            InlineKeyboardButton(text="Закрыть панель", callback_data="close_panel"),

        ],
        "en": [
            InlineKeyboardButton(text="Messages", callback_data="messages"),
            InlineKeyboardButton(text="Database", callback_data="database"),
            InlineKeyboardButton(text="Close panel", callback_data="close_panel"),
        ]
    }

    user_language: str = users_table.get_value("language", "user_id", event.from_user.id)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[user_language][0], buttons[user_language][1])
    builder.row(buttons[user_language][2])
    return builder.as_markup()