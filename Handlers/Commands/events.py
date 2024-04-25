from aiogram import F
from aiogram import types
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery

from config import bot, dispatcher, database as db
import decorators as dec
import Text as txt


@dispatcher.callback_query(F.data == "events")
@dec.update_last_activity
async def events(callback: CallbackQuery) -> None:
    # Load user language.
    user_language: str = db.get_user_language(user_id=callback.from_user.id)
    # Send callback.
    await callback.answer(
        text=txt.translate_text(s, "events", user_language, callback.from_user.id))
    return None


def ru_events(*args) -> str:
    return \
        f"В разработке."


def en_events(*args) -> str:
    return \
        f"In development."


s: dict = {
    "events": {
        "ru": ru_events,
        "en": en_events
    }
}