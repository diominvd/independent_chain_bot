from aiogram import F
from aiogram.types import CallbackQuery

from modules.main import MainModule
from utils import translate


@MainModule.router.callback_query(F.data == "events")
async def support(callback: CallbackQuery) -> None:
    events: list = []
    strings: dict[str, dict] = {
        "events": {
            "ru": "Нет активных событий.",
            "en": "There are no active events."
        }
    }

    await callback.message.edit_text(
        text=translate(callback, strings, "events"),
        reply_markup=MainModule.modules["events"].keyboard(callback)
    )