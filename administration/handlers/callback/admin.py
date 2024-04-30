from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from administration.handlers import admin_router
from administration.middlewares.send_admin_panel import send_admin_panel
from administration.states import AdminStates


@admin_router.callback_query(F.data == "admin")
async def admin_panel(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.answer(show_alert=False)
    await state.set_state(AdminStates.admin_panel)
    await send_admin_panel(callback, state)
    return None