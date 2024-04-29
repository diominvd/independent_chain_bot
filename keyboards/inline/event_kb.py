from aiogram.types import InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import database
from keyboards.button_constructor import button


def event_kb(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [button(signature="Назад", callback="events_menu")],
        "en": [button(signature="Back", callback="events_menu")]
    }
    language: str = database.get_user_language(user_id=event.from_user.id)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[language][0])
    return builder.as_markup()