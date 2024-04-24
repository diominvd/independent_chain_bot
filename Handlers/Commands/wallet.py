import asyncio
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import bot, dispatcher, database as db
from Handlers.Commands.profile import s as s_profile
from Keyboards.Inline import wallet_keyboard, main_keyboard
from States.Default import DefaultStates
import Text as txt


@dispatcher.callback_query(F.data == "wallet")
async def wallet(callback: CallbackQuery, state: FSMContext) -> None:
    # Set wallet wait state.
    await state.set_state(DefaultStates.get_wallet)
    # Stop callback.
    await callback.answer(show_alert=False)
    # Update last user activity.
    db.update_last_activity(user_id=callback.from_user.id)
    # Load user language.
    user_language: str = db.get_user_language(user_id=callback.from_user.id)
    # Load user wallet.
    wallet_address: str = db.get_user_wallet(user_id=callback.from_user.id)[0][0]
    # Check user wallet address exists.
    key = "no_wallet" if wallet_address == "" else "yes_wallet"
    await bot.edit_message_text(
        text=txt.translate_text(s, key, user_language),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id)
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=wallet_keyboard(user_language))
    return None


@dispatcher.message(StateFilter(DefaultStates.get_wallet))
async def wait_wallet(message: Message, state: FSMContext):
    # Clear all states.
    await state.clear()
    # Update last user activity.
    db.update_last_activity(user_id=message.from_user.id)
    # Load user language.
    user_language: str = db.get_user_language(user_id=message.from_user.id)
    # Get wallet address from message.
    address: str = message.text
    # Update user wallet in database.
    db.update_wallet(user_id=message.from_user.id, wallet=address)
    await message.answer(
        text=txt.translate_text(s, "wallet_accepted", user_language, message.from_user.id))
    # Save message id for future deletes.
    message_id: int = message.message_id
    # Delete wallet state messages.
    await bot.delete_message(chat_id=message.from_user.id, message_id=message_id)
    await asyncio.sleep(2)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message_id+1)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message_id-1)
    # Return profile.
    await bot.send_message(
        chat_id=message.from_user.id,
        text=txt.translate_text(s_profile, "profile", user_language, message.from_user.id),
        reply_markup=main_keyboard(user_id=message.from_user.id, language=user_language))
    return None


def ru_request_wallet(*args) -> str:
    return f"Отправьте адрес кошелька в чат с ботом Ton Space, чтобы привязать его к профилю."


def en_request_wallet(*args) -> str:
    return f"Send the wallet address to the chat with the Ton Space bot to link it to your profile."


def ru_request_new_wallet(*args) -> str:
    return f"К вашему профилю уже привязан адрес кошелька Ton Space. Чтобы привязать новый - отправьте адрес кошелька в чат с ботом Ton Space."


def en_request_new_wallet(*args) -> str:
    return f"The Ton Space wallet address is already linked to your profile. To link a new one, send the wallet address to the chat with the Ton Space bot."


def ru_wallet_accepted(*args) -> str:
    return f"Адрес кошелька успешно привязан ✨"


def en_wallet_accepted(*args) -> str:
    return f"The wallet address has been successfully linked ✨"


s: dict = {
    "no_wallet": {
        "ru": ru_request_wallet,
        "en": en_request_wallet
    },
    "yes_wallet": {
        "ru": ru_request_new_wallet,
        "en": en_request_new_wallet
    },
    "wallet_accepted": {
        "ru": ru_wallet_accepted,
        "en": en_wallet_accepted
    }
}