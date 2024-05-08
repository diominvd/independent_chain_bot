from aiogram.types import Message, CallbackQuery

from core.config import users_table


class Translator:
    @staticmethod
    def text(event: Message | CallbackQuery, strings: dict, key: str) -> str:
        user_language: str = users_table.get_value("language", "user_id", event.from_user.id)
        return strings[key][user_language]