from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.config import users_table


def keyboard(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Поддержка", url="https://t.me/diominvd"),
            InlineKeyboardButton(text="Пользовательское соглашение", url="https://teletype.in/@inch_ton/user_agreement_ru"),
            InlineKeyboardButton(text="Назад", callback_data="profile")
        ],
        "en": [
            InlineKeyboardButton(text="Support", url="https://t.me/diominvd"),
            InlineKeyboardButton(text="User agreement", url="https://teletype.in/@inch_ton/user_agreement_en"),
            InlineKeyboardButton(text="Back", callback_data="profile")
        ]
    }

    user_language: str = users_table.get_value("language", "user_id", event.from_user.id)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[user_language][0])
    builder.row(buttons[user_language][1])
    builder.row(buttons[user_language][2])
    return builder.as_markup()