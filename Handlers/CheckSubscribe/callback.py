from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

import text
import utils as u
from Handlers.CheckSubscribe.strings import strings
from Handlers.Start.strings import strings as start_strings
from States import DefaultStates
from config import bot, dispatcher, database as db


@dispatcher.callback_query(F.data == "check_subscribe", StateFilter(DefaultStates.check_subscribe))
@u.update_last_activity
async def subscribe_callback(event: CallbackQuery, state: FSMContext) -> None:
    user_language: str = db.get_user_language(user_id=event.from_user.id)
    # Check user subscribe on channels.
    if not await u.check_subscribe(user_id=event.from_user.id, language=user_language):
        await event.answer(text=text.translate_text(strings, "check_error", user_language))
    else:
        await event.answer(text=text.translate_text(strings, "check_success", user_language))
        # Delete /start message and message with channels.
        await bot.delete_message(chat_id=event.from_user.id, message_id=event.message.message_id)
        await bot.delete_message(chat_id=event.from_user.id, message_id=event.message.message_id - 1)
        # Send start message.
        await bot.send_message(
            chat_id=event.from_user.id,
            text=text.translate_text(start_strings, "start", user_language)
        )
        # Clear states.
        await state.clear()
    return None