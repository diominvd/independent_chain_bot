import datetime

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from core.config import users_table
from modules import MainModuleStates
from modules.main import MainModule
from translator import Translator


@MainModule.router.callback_query(F.data == "codes")
@users_table.update_last_activity
async def codes(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "codes": {
            "ru": "Отправьте 16-ти значный код для его активации 🔠",
            "en": "Send a 16-digit code to activate it 🔠"
        },
        "limit": {
            "ru": "Доступна только одна активация промокода в сутки 🕒",
            "en": "Only one promo code activation per day is available 🕒"
        }
    }

    current_time: datetime = datetime.datetime.now()
    last_activate_time: datetime = users_table.get_last_code_activate(callback.from_user.id)[0]
    time_difference: datetime = (current_time - last_activate_time).total_seconds()

    # Check last activate time.
    if time_difference > 86400:
        await callback.answer(show_alert=False)
        await state.set_state(MainModuleStates.codes)

        await callback.message.edit_text(
            text=Translator.text(callback, strings, "codes"),
            reply_markup=MainModule.modules["codes"].keyboard_back(callback, "events"))
        return None
    else:
        await callback.answer(
            text=Translator.text(callback, strings, "limit"),
            show_alert=True)
        return None