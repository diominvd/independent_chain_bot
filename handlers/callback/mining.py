from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import database
from handlers.callback import callback_router
from utils.translator import translate


@callback_router.callback_query(F.data == "mining")
@database.update_activity
async def mining_callback(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "alert": {
            "ru": f"В разработке.",
            "en": f"In development."
        }
    }

    await callback.answer(text=translate(callback, strings["alert"]))
    return None