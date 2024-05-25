from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils import Translator


def keyboard(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Обновить", callback_data="mining"),
            InlineKeyboardButton(text="Собрать", callback_data="claim"),
            InlineKeyboardButton(text="Улучшения", callback_data="upgrades"),
            InlineKeyboardButton(text="Руководство", url="https://teletype.in/@inch_ton/inch_mining_ru"),
            InlineKeyboardButton(text="Назад", callback_data="profile"),
        ],
        "en": [
            InlineKeyboardButton(text="Refresh", callback_data="mining"),
            InlineKeyboardButton(text="Claim", callback_data="claim"),
            InlineKeyboardButton(text="Upgrades", callback_data="upgrades"),
            InlineKeyboardButton(text="Manual", url="https://teletype.in/@inch_ton/inch_mining_en"),
            InlineKeyboardButton(text="Back", callback_data="profile"),
        ]
    }

    language: str = Translator.language(event)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[language][0])
    builder.row(buttons[language][1])
    builder.row(buttons[language][2])
    builder.row(buttons[language][3])
    builder.row(buttons[language][4])
    return builder.as_markup()