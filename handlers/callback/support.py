from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import database
from handlers.callback import callback_router
from keyboards.inline.infrormation_kb import information_kb
from utils.translator import translate


@callback_router.callback_query(F.data == "information")
@database.update_activity
async def support_callback(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "support": {
            "ru": "",
            "en": ""
        }
    }