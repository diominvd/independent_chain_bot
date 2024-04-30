from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from administration.handlers import admin_router
from administration.keyboards.mail_kb import mail_kb
from administration.states import AdminStates
from markdown import markdown
from utils.translator import translate


@admin_router.callback_query(F.data == "mail")
async def mail(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "request_username": {
            "ru": f"Отправьте имя имя пользователя получателя в формате {markdown.monospaced('@username')}.",
            "en": f"Send the recipient's username in the format {markdown.monospaced('@username')}."
        }
    }

    await state.set_state(AdminStates.mail_username)
    await callback.answer(show_alert=False)
    await callback.message.edit_text(
        text=translate(callback, strings["request_username"]),
        reply_markup=mail_kb(callback)
    )
    return None