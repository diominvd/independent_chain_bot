from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils import Translator


def keyboard(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Пользовательское соглашение", url="https://teletype.in/@inch_ton/user_agreement_ru"),
            InlineKeyboardButton(text="Канал проекта", url="https://t.me/inch_ton")
        ],
        "en": [
            InlineKeyboardButton(text="User agreement", url="https://teletype.in/@inch_ton/user_agreement_en"),
            InlineKeyboardButton(text="Project channel", url="https://t.me/inch_ton")
        ]
    }

    language: str = Translator.language(event)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[language][0])
    builder.row(buttons[language][1])
    return builder.as_markup()