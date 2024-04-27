from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import Text as txt
import utils as u
from Handlers.Start import strings
from Keyboards.Inline.subscribe import keyboard
from States import DefaultStates
from config import bot, dispatcher, database as db


@dispatcher.message(Command("start"))
@u.update_last_activity
async def start(message: Message, state: FSMContext) -> None:
    await state.clear()
    # Check user existence in database.
    if not db.check_user_existence(message.from_user.id):
        db.add_new_user(user_data=u.pack_user_data(message))
        db.check_user_inviter(user_id=message.from_user.id,
                              inviter_id=u.get_inviter_id(message))
    user_language: str = db.get_user_language(user_id=message.from_user.id)
    # Check user subscribe on channels.
    if not await u.check_subscribe(user_id=message.from_user.id, language=user_language):
        # Send message with channels.
        await message.answer(
            text=txt.translate_text(strings, "alert", user_language),
            reply_markup=keyboard(language=user_language))
        await state.set_state(DefaultStates.check_subscribe)
    else:
        # Delete message with /start command.
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
        await bot.send_message(
            chat_id=message.from_user.id,
            text=txt.translate_text(strings, "start", user_language))
    return None