from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from config import bot, dispatcher, database as db
import decorators as dec
from Keyboards.Inline import main_keyboard
import Text as txt


@dispatcher.callback_query(F.data == "support")
@dec.update_last_activity
async def support(event: CallbackQuery, state: FSMContext) -> None:
    # Stop callback.
    await event.answer(show_alert=False)
    # Load user language.
    user_language: str = db.get_user_language(user_id=event.from_user.id)
    await bot.edit_message_text(
        text=txt.translate_text(s, "support", user_language, event.from_user.id),
        chat_id=event.from_user.id,
        message_id=event.message.message_id)
    await bot.edit_message_reply_markup(
        chat_id=event.from_user.id,
        message_id=event.message.message_id,
        reply_markup=main_keyboard(user_id=event.from_user.id, language=user_language))
    return None


def ru_support(*args) -> str:
    return \
        f"В случае возникновения ошибок или каких-либо проблем с ботом просим написать вас в поддержку: @diominvdev.\n\nТекущая версия бота: 2.2 🤖"


def en_support(*args) -> str:
    return \
        f"In case of errors or any problems with the bot, please write to support: @diominvdev.\n\nThe current version of the bot is 2.2 🤖"


s: dict = {
    "support": {
        "ru": ru_support,
        "en": en_support
    }
}
