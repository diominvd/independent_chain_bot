from aiogram.types import Message, CallbackQuery

from core.config import UsersTable


class Translator:
    @staticmethod
    def language(event: Message | CallbackQuery):
        language: str = UsersTable.select(("language",), "user_id", event.from_user.id)[0]
        return language

    @staticmethod
    def text(event: Message | CallbackQuery, strings: dict, key: str) -> str:
        language: str = UsersTable.select(("language", ), "user_id", event.from_user.id)[0]
        if language not in ["ru", "en"]:
            language: str = "en"
        return strings[key][language]