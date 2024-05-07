from aiogram import F
from aiogram.types import CallbackQuery

from modules.main import MainModule
from utils import translate


@MainModule.router.callback_query(F.data == "support")
async def support(callback: CallbackQuery) -> None:
    strings: dict[str, dict] = {
        "support": {
            "ru": f"В случае возникновения ошибок или каких-либо проблем с ботом просим написать вас в поддержку.\n\n"
                  f"Опишите проблему и приложите дополнительные материалы (фото, видео) для скорейшего решения вашей проблемы.\n\n"
                  f"Версия бота: 4.1 🤖",
            "en": f"In case of errors or any problems with the bot, please write to support.\n\n"
                  f"Describe the problem and attach additional materials (photos, videos) to solve your problem as soon as possible.\n\n"
                  f"Bot version: 4.1 🤖"
        }
    }

    await callback.message.edit_text(
        text=translate(callback, strings, "support"),
        reply_markup=MainModule.modules["support"].keyboard(callback)
    )