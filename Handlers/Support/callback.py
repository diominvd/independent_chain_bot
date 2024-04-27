from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

import Text as txt
import utils as u
from Handlers.Support import strings
from Keyboards.Inline.menu import keyboard
from States import DefaultStates
from config import dispatcher, database as db


@dispatcher.callback_query(F.data == "support")
@u.update_last_activity
async def support(event: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(DefaultStates.support)
    await event.answer(show_alert=False)
    user_language: str = db.get_user_language(user_id=event.from_user.id)
    await event.message.edit_text(
        text=txt.translate_text(strings, "support", user_language, event.from_user.id),
        reply_markup=keyboard(user_id=event.from_user.id, language=user_language))
    return None