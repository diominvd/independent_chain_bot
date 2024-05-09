from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from core.config import users_table
from modules.main import MainModule
from translator import Translator


@MainModule.router.callback_query(F.data == "support")
@users_table.update_last_activity
async def support(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "support": {
            "ru": (f"В случае возникновения ошибок или каких-либо проблем с ботом просим написать вас в поддержку.\n\n"
                   f"Опишите проблему и приложите дополнительные материалы (фото, видео) для скорейшего решения вашей проблемы.\n\n"
                   f"Версия бота: 5.0 🤖"),
            "en": (f"In case of errors or any problems with the bot, please write to support.\n\n"
                   f"Describe the problem and attach additional materials (photos, videos) to solve your problem as soon as possible.\n\n"
                   f"Bot version: 5.0 🤖")
        }
    }

    await callback.message.edit_text(
        text=Translator.text(callback, strings, "support"),
        reply_markup=MainModule.modules["support"].keyboard(callback))
    return None
