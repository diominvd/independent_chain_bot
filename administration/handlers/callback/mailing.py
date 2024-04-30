from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from administration.handlers import admin_router
from administration.keyboards.mail_kb import mail_kb
from administration.states import AdminStates
from utils.translator import translate


@admin_router.callback_query(StateFilter(AdminStates.admin_panel), F.data == "mailing")
async def mailing_ru(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "request_ru_message": {
            "ru": "Отправьте текст сообщения на русском языке.",
            "en": "Send the text of the message in Russian."
        }
    }

    await state.set_state(AdminStates.mailing_ru)
    await callback.answer(show_alert=False)
    await callback.message.edit_text(
        text=translate(callback, strings["request_ru_message"]),
        reply_markup=mail_kb(callback)
    )