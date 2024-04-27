from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def keyboard(language: str) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    names: dict = {
        "ru": ["Основной канал", "Канал разработки", "Твиттер", "TonScan", "Whitepaper проекта", "Назад"],
        "en": ["Project channel", "Dev channel", "Twitter", "TonScan", "Project whitepaper", "Back"]
    }
    links: dict = {
        "ru": ["https://t.me/inch_ru", "https://t.me/diominvdev", "https://x.com/inch_coin", "https://tonscan.org/jetton/EQDRaPxN8MkJOJYX-adlBBFnhMlHfPzIgD7NtyM0dtiauCZL?clckid=e9ddf724", "https://github.com/diominvd/independent_chain"],
        "en": ["https://t.me/inch_en", "https://t.me/diominvdev", "https://x.com/inch_coin", "https://tonscan.org/jetton/EQDRaPxN8MkJOJYX-adlBBFnhMlHfPzIgD7NtyM0dtiauCZL?clckid=e9ddf724", "https://github.com/diominvd/independent_chain"]
    }

    builder.row(
        InlineKeyboardButton(text=names[language][0], url=links[language][0]),
        InlineKeyboardButton(text=names[language][1], url=links[language][1]))
    builder.row(
        InlineKeyboardButton(text=names[language][2], url=links[language][2]),
        InlineKeyboardButton(text=names[language][3], url=links[language][3]))
    builder.row(
        InlineKeyboardButton(text=names[language][4], url=links[language][4]))
    builder.row(
        InlineKeyboardButton(text=names[language][5], callback_data="profile"))
    return builder.as_markup()