from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from administration.handlers import admin_router
from administration.states import AdminStates
from middlewares.send_profile import send_profile
from utils.translator import translate


@admin_router.callback_query(StateFilter(AdminStates.admin_panel), F.data == "admin_exit")
async def admin_exit(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "panel_closed": {
            "ru": "Панель администратора закрыта.",
            "en": "The admin panel is closed."
        }
    }

    await state.clear()
    await callback.answer(show_alert=False)
    await callback.answer(text=translate(callback, strings["panel_closed"]))
    await send_profile(callback)
    return None