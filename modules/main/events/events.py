from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from core.config import users_table
from markdown import Markdown
from modules.main import MainModule
from translator import Translator


@MainModule.router.callback_query(F.data == "events")
@users_table.check_wallet_black_list
@users_table.update_last_activity
async def events_(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "events": {
            "ru": (f"В данном разделе находятся актуальные события и активности 🥳\n\n"
                   f"Для просмотра конкретного события выберите соответствующую кнопку.\n\n"
                   f"{Markdown.bold('Текущие события')}:\n"
                   f"• Слоты - испытай свою удачу и заработай $tINCH."),
            "en": (f"This section contains current events and activities 🥳\n\n"
                   f"To view a specific event, select the appropriate button.\n\n"
                   f"{Markdown.bold('Current Events')}:\n"
                   f"• Slots - try your luck and earn $tINCH.")
        }
    }

    await callback.answer(show_alert=False)

    await callback.message.edit_text(
        text=Translator.text(callback, strings, "events"),
        reply_markup=MainModule.modules["events"].keyboard(callback))
    return None