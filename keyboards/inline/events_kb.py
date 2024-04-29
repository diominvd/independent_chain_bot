from aiogram.types import InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import database
from keyboards.button_constructor import button


def events_kb(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [button(signature="💎 Розыгрыш NFT", callback="raffle_nft"),
               button(signature="Назад", callback="profile")],
        "en": [button(signature="💎 Raffle NFT", callback="raffle_nft"),
               button(signature="Back", callback="profile")]
    }
    language: str = database.get_user_language(user_id=event.from_user.id)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[language][0])
    builder.row(buttons[language][1])
    return builder.as_markup()