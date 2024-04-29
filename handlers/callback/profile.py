from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import database
from handlers.callback import callback_router
from middlewares.send_profile import send_profile


@callback_router.callback_query(F.data == "profile")
@database.update_activity
async def profile_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await send_profile(callback)
    return None