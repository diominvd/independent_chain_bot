import asyncio

from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import text
import utils as u
from Handlers.Profile.strings import strings as profile_strings
from Handlers.Wallet.strings import strings
from Keyboards.Inline.menu import keyboard
from States import DefaultStates
from config import bot, dispatcher, database as db


@dispatcher.message(StateFilter(DefaultStates.wallet))
@u.update_last_activity
async def wait_wallet(event: Message, state: FSMContext):
    user_language: str = db.get_user_language(user_id=event.from_user.id)
    await state.set_state(DefaultStates.profile)
    wallet_address: str = event.text
    db.update_wallet(user_id=event.from_user.id, wallet=wallet_address)
    # Save message id for future deletes.
    message_id: int = event.message_id
    # Delete wallet state messages.
    await bot.delete_message(chat_id=event.from_user.id, message_id=message_id)
    await bot.edit_message_text(
        chat_id=event.from_user.id,
        message_id=message_id-1,
        text=text.translate_text(strings, "wallet_accepted", user_language, event.from_user.id)
    )
    await asyncio.sleep(3)
    # Return profile.
    await bot.edit_message_text(
        chat_id=event.from_user.id,
        message_id=message_id-1,
        text=text.translate_text(profile_strings, "profile", user_language, event.from_user.id),
        reply_markup=keyboard(user_id=event.from_user.id, language=user_language)
    )
    return None