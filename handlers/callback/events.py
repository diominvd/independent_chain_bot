from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import database
from handlers.callback import callback_router
from keyboards.inline.events_kb import events_kb
from keyboards.inline.wallet_kb import wallet_kb
from states import BotStates, EventsStates
from utils.translator import translate


@callback_router.callback_query(F.data == "events_menu")
@database.update_activity
async def events_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(EventsStates.events_menu)
    strings: dict[str, dict] = {
        "description": {
            "ru": "Выберите необходимое событие для просмотра подробностей.",
            "en": "Select the required event to view the details."
        }
    }

    await callback.answer(show_alert=False)
    await callback.message.edit_text(
        text=translate(callback, strings["description"]),
        reply_markup=events_kb(callback)
    )
    return None