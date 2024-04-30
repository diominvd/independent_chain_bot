from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import database
from handlers.callback import callback_router
from keyboards.inline.events_menu_kb import events_kb
from states import BotStates
from utils.translator import translate


@callback_router.callback_query(F.data == "events_menu")
@database.update_activity
async def events_callback(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "description": {
            "ru": "В нашем сообществе регулярно проходя различные события с призами и наградами.\n\n"
                  "Следите за новостями, чтобы не упустить шанс и принять участие.",
            "en": "Our community regularly hosts various events with prizes and awards.\n\n"
                  "Follow the news so as not to miss the chance and take part."
        }
    }

    await state.set_state(BotStates.events_menu)
    await callback.answer(show_alert=False)
    await callback.message.edit_text(
        text=translate(callback, strings["description"]),
        reply_markup=events_kb(callback)
    )
    return None