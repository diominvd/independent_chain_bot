from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.config import users_table


def keyboard(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Статистика", callback_data="statistics"),
            InlineKeyboardButton(text="Промокоды", callback_data="_codes"),
            InlineKeyboardButton(text="Получить значение", callback_data="get_values"),
            InlineKeyboardButton(text="Изменить значение", callback_data="change_values"),
            InlineKeyboardButton(text="Назад", callback_data="panel"),

        ],
        "en": [
            InlineKeyboardButton(text="Statistics", callback_data="statistics"),
            InlineKeyboardButton(text="Promo codes", callback_data="_codes"),
            InlineKeyboardButton(text="Get value", callback_data="get_values"),
            InlineKeyboardButton(text="Change value", callback_data="change_values"),
            InlineKeyboardButton(text="Back", callback_data="panel"),
        ]
    }

    user_language: str = users_table.get_value("language", "user_id", event.from_user.id)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[user_language][0], buttons[user_language][1])
    builder.row(buttons[user_language][2], buttons[user_language][3])
    builder.row(buttons[user_language][4])
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


def keyboard_back(event: Message | CallbackQuery, callback_data: str) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Назад", callback_data=callback_data),

        ],
        "en": [
            InlineKeyboardButton(text="Back", callback_data=callback_data),
        ]
    }

    user_language: str = users_table.get_value("language", "user_id", event.from_user.id)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[user_language][0])
    return builder.as_markup()


def keyboard_codes(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Сгенерировать", callback_data="generate_codes"),
            InlineKeyboardButton(text="Получить", callback_data="get_codes"),
            InlineKeyboardButton(text="Назад", callback_data="database"),
        ],
        "en": [
            InlineKeyboardButton(text="Generate", callback_data="generate_codes"),
            InlineKeyboardButton(text="Get", callback_data="get_codes"),
            InlineKeyboardButton(text="Back", callback_data="database"),
        ]
    }

    user_language: str = users_table.get_value("language", "user_id", event.from_user.id)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[user_language][0], buttons[user_language][1])
    builder.row(buttons[user_language][2])
    return builder.as_markup()