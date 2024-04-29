from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.button_constructor import button


def subscribe_kb(language: str) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [button(signature="Канал проекта", url="https://t.me/inch_ru"),
               button(signature="Проверить", callback="check_subscribe")],
        "en": [button(signature="Project channel", url="https://t.me/inch_en"),
               button(signature="Check", callback="check_subscribe")]
    }
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[language][0])
    builder.row(buttons[language][1])
    return builder.as_markup()