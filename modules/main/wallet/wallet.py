from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from core.config import users_table
from modules import MainModuleStates
from modules.main import MainModule
from translator import Translator


@MainModule.router.callback_query(F.data == "wallet")
@users_table.check_wallet_black_list
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