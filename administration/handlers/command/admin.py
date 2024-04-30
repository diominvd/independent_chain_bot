from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from administration.handlers import admin_router
from administration.middlewares.send_admin_panel import send_admin_panel
from administration.states import AdminStates
from secrets import admins


@admin_router.message(Command("admin"))
async def admin_panel(message: Message, state: FSMContext) -> None:
    await state.clear()
    if message.from_user.id in [i for i in admins.values()]:
        await state.set_state(AdminStates.admin_panel)
        await send_admin_panel(message, state)
    return None