from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from core.config import users_table
from markdown import Markdown
from modules.main import MainModule
from translator import Translator


@MainModule.router.callback_query(F.data == "support")
@users_table.check_wallet_black_list
@users_table.update_last_activity
async def support(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "support": {
            "ru": (f"Перед началом использования бота настоятельно рекомендуем ознакомиться с "
                   f"{Markdown.url('пользовательским соглашением', url='https://teletype.in/@inch_ton/user_agreement_ru')} проекта.\n\n"
                   f"В случае возникновения ошибок или каких-либо проблем с ботом просим написать вас в поддержку.\n\n"
                   f"Опишите проблему и приложите дополнительные материалы (фото, видео) для скорейшего решения вашей проблемы.\n\n"
                   f"Версия бота: 6.0 🤖"),
            "en": (f"Before using the bot, we strongly recommend that you familiarize yourself with the "
                   f"{Markdown.url('user agreement', url='https://teletype.in/@inch_ton/user_agreement_en')} of the project.\n\n"
                   f"In case of errors or any problems with the bot, please write to support.\n\n"
                   f"Describe the problem and attach additional materials (photos, videos) to solve your problem as soon as possible.\n\n"
                   f"Bot version: 6.0 🤖")
        }
    }

    await callback.message.edit_text(
        text=Translator.text(callback, strings, "support"),
        reply_markup=MainModule.modules["support"].keyboard(callback))
    return None
