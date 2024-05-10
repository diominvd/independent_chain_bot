import asyncio
from multiprocessing import Process

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from core.config import users_table, bot
from modules import MainModuleStates
from modules.main import MainModule
from translator import Translator


@MainModule.router.callback_query(F.data == "wallet")
@users_table.update_last_activity
async def wallet(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "information": {
            "ru": "Для привязки кошелька отправьте адрес вашего кошелька Ton Space.",
            "en": "To link a wallet, send the address of your Ton Space wallet."
        }
    }

    # Stop alert:
    await callback.answer(show_alert=False)
    await state.update_data(wallet_message=callback.message.message_id)
    await state.set_state(MainModuleStates.wallet)

    await callback.message.edit_text(
        text=Translator.text(callback, strings, "information"),
        reply_markup=MainModule.modules["wallet"].keyboard_cancel(callback))
    return None


@MainModule.router.message(StateFilter(MainModuleStates.wallet))
@users_table.update_last_activity
async def wallet(message: Message, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "success": {
            "ru": "Кошелёк успешно подключён ✅",
            "en": "The wallet has been successfully connected ✅"
        },
        "fail": {
            "ru": ("Некорректный адрес кошелька 🚫\n"
                   "Длина адреса должна быть равна 48 знакам. Проверьте правильность написания адреса и повторите попытку."),
            "en": ("Invalid wallet address 🚫\n"
                   "The length of the address must be 48 characters. Check that the address is spelled correctly and try again.")
        }
    }

    data: dict = await state.get_data()

    wallet_address: str = message.text

    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id)

    if len(wallet_address) == 48:
        users_table.update_wallet(message.from_user.id, wallet_address)

        await bot.edit_message_text(
            chat_id=message.from_user.id,
            message_id=data["wallet_message"],
            text=Translator.text(message, strings, "success"),
            reply_markup=MainModule.modules["wallet"].keyboard_finish(message))
    else:
        await bot.edit_message_text(
            chat_id=message.from_user.id,
            message_id=data["wallet_message"],
            text=Translator.text(message, strings, "fail"),
            reply_markup=MainModule.modules["wallet"].keyboard_cancel(message))
    return None