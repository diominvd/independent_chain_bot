from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

import Text as txt
import utils as u
from Handlers.Events import strings
from config import dispatcher, database as db


@dispatcher.callback_query(F.data == "events")
@u.update_last_activity
async def events(event: CallbackQuery, state: FSMContext) -> None:
    user_language: str = db.get_user_language(user_id=event.from_user.id)
    await event.answer(
        text=txt.translate_text(strings, "events", user_language, event.from_user.id))
    return None