from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import database
from handlers.callback import callback_router
from middlewares.send_profile import send_profile


@callback_router.callback_query(F.data == "profile")
@database.update_activity
async def profile_callback(callback: CallbackQuery, state: FSMContext) -> None:
    language: str = database.get_user_language(user_id=callback.from_user.id)
    await send_profile(callback, language)
    return None