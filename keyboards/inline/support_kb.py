from aiogram.types import InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import database
from keyboards.button_constructor import button


def support_kb(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [button(signature="Поддержка", url="https://t.me/diominvd"),
               button(signature="Исходный код", url="https://github.com/diominvd/independent_chain_bot"),
               button(signature="Назад", callback="profile")],
        "en": [button(signature="Support", url="https://t.me/diominvd"),
               button(signature="Source code", url="https://github.com/diominvd/independent_chain_bot"),
               button(signature="Back", callback="profile")]
    }
    language: str = database.get_user_language(user_id=event.from_user.id)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[language][0], buttons[language][1])
    builder.row(buttons[language][2])
    return builder.as_markup()