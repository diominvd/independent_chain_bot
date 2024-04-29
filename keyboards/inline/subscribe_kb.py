from aiogram.types import InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import database
from keyboards.button_constructor import button


def subscribe_kb(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [button(signature="Канал проекта", url="https://t.me/inch_ru"),
               button(signature="Проверить", callback="check_subscribe")],
        "en": [button(signature="Project channel", url="https://t.me/inch_en"),
               button(signature="Check", callback="check_subscribe")]
    }

    language: str = database.get_user_language(user_id=event.from_user.id)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[language][0])
    builder.row(buttons[language][1])
    return builder.as_markup()