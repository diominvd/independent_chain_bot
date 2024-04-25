from aiogram import F
from aiogram import types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import bot, dispatcher, database as db
import decorators as dec
import Text as txt


@dispatcher.callback_query(F.data == "events")
@dec.update_last_activity
async def events(event: CallbackQuery, state: FSMContext) -> None:
    # Load user language.
    user_language: str = db.get_user_language(user_id=event.from_user.id)
    # Send callback.
    await event.answer(
        text=txt.translate_text(s, "events", user_language, event.from_user.id))
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