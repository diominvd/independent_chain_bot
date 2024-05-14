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


def keyboard_geckoshi(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Канал Geckoshi", url="https://t.me/geckoshi_coin"),
            InlineKeyboardButton(text="Проверить подписку", callback_data="check_subscribe"),
            InlineKeyboardButton(text="Назад", callback_data="events"),

        ],
        "en": [
            InlineKeyboardButton(text="Geckoshi channel", url="https://t.me/geckoshi_coin"),
            InlineKeyboardButton(text="Check subscribe", callback_data="check_subscribe"),
            InlineKeyboardButton(text="Back", callback_data="events"),
        ]
    }

    user_language: str = users_table.get_value("language", "user_id", event.from_user.id)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[user_language][0])
    builder.row(buttons[user_language][1])
    builder.row(buttons[user_language][2])
    return builder.as_markup()