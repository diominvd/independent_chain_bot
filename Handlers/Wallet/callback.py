from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

import text
import utils as u
from Handlers.Wallet.strings import strings
from Keyboards.Inline.wallet import keyboard
from States import DefaultStates
from config import dispatcher, database as db


@dispatcher.callback_query(F.data == "wallet")
@u.update_last_activity
async def wallet(event: CallbackQuery, state: FSMContext) -> None:
    user_language: str = db.get_user_language(user_id=event.from_user.id)
    wallet_address: str = db.get_user_wallet(user_id=event.from_user.id)[0][0]
    await state.set_state(DefaultStates.wallet)
    await event.answer(show_alert=False)
    # Check user wallet address exists.
    key = "no_wallet" if wallet_address is None else "yes_wallet"
    await event.message.edit_text(
        text=text.translate_text(strings, key, user_language),
        reply_markup=keyboard(user_language)
    )
    return None