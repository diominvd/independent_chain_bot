from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.config import users_table


def keyboard(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Личное сообщение", callback_data="mail"),
            InlineKeyboardButton(text="Массовая рассылка", callback_data="mailing"),
            InlineKeyboardButton(text="Назад", callback_data="panel"),

        ],
        "en": [
            InlineKeyboardButton(text="Mailing", callback_data="mail"),
            InlineKeyboardButton(text="Database", callback_data="mailing"),
            InlineKeyboardButton(text="Back", callback_data="panel"),
        ]
    }

    user_language: str = users_table.get_value("language", "user_id", event.from_user.id)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[user_language][0], buttons[user_language][1])
    builder.row(buttons[user_language][2])
    return builder.as_markup()


def keyboard_close(event: Message | CallbackQuery, callback_data: str) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Закрыть", callback_data=callback_data),
        ],
        "en": [
            InlineKeyboardButton(text="Close", callback_data=callback_data),
        ]
    }

    user_language: str = users_table.get_value("language", "user_id", event.from_user.id)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[user_language][0])
    return builder.as_markup()


def keyboard_cancel(event: Message | CallbackQuery, callback_data: str) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Отмена", callback_data=callback_data),
        ],
        "en": [
            InlineKeyboardButton(text="Cancel", callback_data=callback_data),
        ]
    }

    user_language: str = users_table.get_value("language", "user_id", event.from_user.id)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[user_language][0])
    return builder.as_markup()


def keyboard_mail_constructor(name: str, url: str) -> InlineKeyboardMarkup | None:
    if name != "None" and url != "None":
        buttons: list = [InlineKeyboardButton(text=name, url=url)]

        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        builder.row(buttons[0])
        return builder.as_markup()
    else:
        return None