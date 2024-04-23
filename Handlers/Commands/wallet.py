import asyncio

from aiogram import F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery


from config import bot, dispatcher, database as db
from States.Default import DefaultStates
import Text as txt


@dispatcher.callback_query(F.data == "wallet")
async def wallet(callback: CallbackQuery, state: FSMContext) -> None:
    # Update last user activity.
    db.update_last_activity(user_id=callback.from_user.id)
    # Load user language.
    user_language: str = db.get_user_language(user_id=callback.from_user.id)
    # Send message with wallet request.
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=txt.translate_text(s, "wallet", user_language, callback.from_user.id))
    # Set state for get wallet address.
    await state.set_state(DefaultStates.get_wallet)
    return None


@dispatcher.message(StateFilter(DefaultStates.get_wallet))
async def wait_wallet(message: Message, state: FSMContext):
    # Update last user activity.
    db.update_last_activity(user_id=message.from_user.id)
    # Load user language.
    user_language: str = db.get_user_language(user_id=message.from_user.id)
    # Get wallet address from message.
    address: str = message.text
    # Update user wallet in database.
    db.update_wallet(user_id=message.from_user.id, wallet=address)
    await message.answer(
        text=txt.translate_text(s, "wait_wallet", user_language, message.from_user.id))
    # Delete messages.
    await asyncio.sleep(2)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id+1)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id-1)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    # Clear all states.
    await state.clear()


def ru_request_wallet(*args) -> str:
    return f"Отправьте адрес кошелька Ton Space, чтобы привязать его к профилю."


def en_request_wallet(*args) -> str:
    return f"Send the Ton Space wallet address to link it to your profile."


def ru_wallet_accepted(*args) -> str:
    return f"Адрес кошелька успешно привязан ✨ Обновите профиль."


def en_wallet_accepted(*args) -> str:
    return f"The wallet address has been successfully linked ✨ Update your profile."


s: dict = {
    "wallet": {
        "ru": ru_request_wallet,
        "en": en_request_wallet
    },
    "wait_wallet": {
        "ru": ru_wallet_accepted,
        "en": en_wallet_accepted
    }
}