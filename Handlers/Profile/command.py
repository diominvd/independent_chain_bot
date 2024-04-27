from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import Text as txt
import utils as u
from Handlers.Profile import strings
from Keyboards.Inline.menu import keyboard
from States import DefaultStates
from config import bot, dispatcher, database as db


@dispatcher.message(Command("profile"))
@u.update_last_activity
async def profile(event: Message, state: FSMContext) -> None:
    await state.set_state(DefaultStates.profile)
    user_language: str = db.get_user_language(user_id=event.from_user.id)
    # Delete message with /profile command.
    await bot.delete_message(chat_id=event.from_user.id, message_id=event.message_id)
    await bot.send_message(
        chat_id=event.from_user.id,
        text=txt.translate_text(strings, "profile", user_language, event.from_user.id),
        reply_markup=keyboard(user_id=event.from_user.id, language=user_language))
    return None