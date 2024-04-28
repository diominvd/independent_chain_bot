from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

import text
import utils as u
from Handlers.Information.strings import strings
from Keyboards.Inline.information import keyboard
from States import DefaultStates
from config import dispatcher, database as db


@dispatcher.callback_query(F.data == "information")
@u.update_last_activity
async def information(event: CallbackQuery, state: FSMContext) -> None:
    user_language: str = db.get_user_language(user_id=event.from_user.id)
    await state.set_state(DefaultStates.information)
    await event.answer(show_alert=False)
    await event.message.edit_text(
        text=text.translate_text(strings, "information", user_language, event.from_user.id),
        reply_markup=keyboard(language=user_language)
    )
    return None