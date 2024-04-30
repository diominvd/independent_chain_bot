from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import database
from handlers.callback import callback_router
from keyboards.inline.support_kb import support_kb
from utils.translator import translate


@callback_router.callback_query(F.data == "support")
@database.update_activity
async def support_callback(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "support": {
            "ru": f"В случае возникновения ошибок или каких-либо проблем с ботом просим написать вас в поддержку.\n\n"
                  f"Опишите проблему и приложите дополнительные материалы (фото, видео) для скорейшего решения вашей проблемы.\n\n"
                  f"Версия бота: 3.2 🤖",
            "en": f"In case of errors or any problems with the bot, please write to support.\n\n"
                  f"Describe the problem and attach additional materials (photos, videos) to solve your problem as soon as possible.\n\n"
                  f"Bot version: 3.2 🤖"
        }
    }

    await callback.answer(show_alert=False)
    await callback.message.edit_text(
        text=translate(callback, strings["support"]),
        reply_markup=support_kb(callback)
    )
    return None