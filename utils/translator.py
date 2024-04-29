from aiogram.types import Message, CallbackQuery

from config import database


def translate(event: Message | CallbackQuery, text: dict) -> str:
    language: str = database.get_user_language(user_id=event.from_user.id)
    return text[language]