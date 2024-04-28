from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import text
import utils as u
from Handlers.Start.strings import strings
from Keyboards.Inline.subscribe import keyboard
from States import DefaultStates
from config import bot, dispatcher, database as db, event_database as edb


@dispatcher.message(Command("start"))
@u.update_last_activity
async def start(event: Message, state: FSMContext) -> None:
    await state.clear()
    # Check user existence in database.
    if not db.check_user_existence(event.from_user.id):
        db.add_new_user(user_data=u.pack_user_data(event))
        db.check_user_inviter(user_id=event.from_user.id, inviter_id=u.get_inviter_id(event))
        edb.update_event_referals(user_id=event.from_user.id, inviter_id=u.get_inviter_id(event))
    user_language: str = db.get_user_language(user_id=event.from_user.id)
    # Check user subscribe on channels.
    if not await u.check_subscribe(user_id=event.from_user.id, language=user_language):
        # Send message with channels.
        await event.answer(
            text=text.translate_text(strings, "alert", user_language),
            reply_markup=keyboard(language=user_language)
        )
        await state.set_state(DefaultStates.check_subscribe)
    else:
        # Delete message with /start command.
        await bot.delete_message(chat_id=event.from_user.id, message_id=event.message_id)
        await bot.send_message(
            chat_id=event.from_user.id,
            text=text.translate_text(strings, "start", user_language)
        )
    return None