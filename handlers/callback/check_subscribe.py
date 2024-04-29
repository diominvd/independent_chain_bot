from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import database, bot
from handlers.callback import callback_router
from middlewares.send_greeting import send_greeting
from middlewares.check_subscribe import check_subscribe
from utils.translator import translate


@callback_router.callback_query(F.data == "check_subscribe")
async def subscribe_callback(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "check_success": {
            "ru": "Проверка пройдена.",
            "en": "The check is passed."
        }
    }
    language: str = database.get_user_language(user_id=callback.from_user.id)
    if await check_subscribe(callback):
        await callback.answer(text=translate(callback, strings["check_success"]))
        await send_greeting(callback)
    return None