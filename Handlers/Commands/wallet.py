import asyncio

from aiogram import F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from Keyboards.Inline import main_keyboard
import Parse as p
from config import bot, dispatcher, database
from States.Default import DefaultStates
import utils as u


@dispatcher.callback_query(F.data == "wallet")
async def wallet(callback: CallbackQuery, state: FSMContext):
    database.update_last_activity(int(callback.from_user.id))
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=u.translate_text(strings, "request_wallet", database.get_user_language(int(callback.from_user.id)), int(callback.from_user.id)),
    )
    await state.set_state(DefaultStates.wallet_state)


@dispatcher.message(StateFilter(DefaultStates.wallet_state))
async def wallet_address(message: Message, state: FSMContext):
    database.update_last_activity(int(message.from_user.id))
    address: str = message.text
    database.update_wallet(int(message.from_user.id), address)
    await message.answer(
        text=u.translate_text(strings, "wallet_accepted", database.get_user_language(int(message.from_user.id)), int(message.from_user.id)),
    )
    await asyncio.sleep(2)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id+1)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id-1)
    # Clear states.
    await state.clear()


def ru_request_wallet(*args) -> str:
    text: str = f"Отправьте адрес кошелька Ton Space, чтобы привязать его к профилю."
    return text


def en_request_wallet(*args) -> str:
    text: str = f"Send the Ton Space wallet address to link it to your profile."
    return text


def ru_wallet_accepted(*args) -> str:
    text: str = f"Адрес кошелька успешно сохранён ✨ Обновите профиль."
    return text


def en_wallet_accepted(*args) -> str:
    text: str = f"The wallet address has been successfully saved ✨ Update your profile."
    return text


strings: dict = {
    "request_wallet": {
        "ru": ru_request_wallet,
        "en": en_request_wallet
    },
    "wallet_accepted": {
        "ru": ru_wallet_accepted,
        "en": en_wallet_accepted
    }
}