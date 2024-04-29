from aiogram.types import InlineKeyboardMarkup, CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import database
from keyboards.button_constructor import button


def information_kb(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [button(signature="Основной канал", url="https://t.me/inch_ru"),
               button(signature="Канал разработки", url="https://t.me/diominvdev"),
               button(signature="Твиттер", url="https://x.com/inch_coin"),
               button(signature="TonScan", url="https://tonscan.org/jetton/EQDRaPxN8MkJOJYX-adlBBFnhMlHfPzIgD7NtyM0dtiauCZL?clckid=e9ddf724"),
               button(signature="Whitepaper проекта", url="https://github.com/diominvd/independent_chain"),
               button(signature="Назад", callback="profile")],
        "en": [button(signature="Project channel", url="https://t.me/inch_en"),
               button(signature="Dev channel", url="https://t.me/diominvdev"),
               button(signature="Twitter", url="https://x.com/inch_coin"),
               button(signature="TonScan", url="https://tonscan.org/jetton/EQDRaPxN8MkJOJYX-adlBBFnhMlHfPzIgD7NtyM0dtiauCZL?clckid=e9ddf724"),
               button(signature="Project whitepaper", url="https://github.com/diominvd/independent_chain"),
               button(signature="Back", callback="profile")]
    }
    language: str = database.get_user_language(user_id=event.from_user.id)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[language][0], buttons[language][1])
    builder.row(buttons[language][2], buttons[language][3])
    builder.row(buttons[language][4])
    builder.row(buttons[language][5])
    return builder.as_markup()