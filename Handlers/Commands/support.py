from aiogram import F
from aiogram.types import Message, CallbackQuery

from config import bot, dispatcher, database as db
from Keyboards.Inline import main_keyboard
import Text as txt


@dispatcher.callback_query(F.data == "support")
async def support(callback: CallbackQuery) -> None:
    # Stop callback.
    await callback.answer(show_alert=False)
    # Update last user activity.
    db.update_last_activity(user_id=callback.from_user.id)
    # Load user language.
    user_language: str = db.get_user_language(user_id=callback.from_user.id)
    await bot.edit_message_text(
        text=txt.translate_text(s, "support", user_language, callback.from_user.id),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id)
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=main_keyboard(user_id=callback.from_user.id, language=user_language))
    return None


def ru_support(*args) -> str:
    return \
        f"В случае возникновения ошибок или каких-либо проблем с ботом просим написать вас в поддержку: @diominvdev.\n\nТекущая версия бота: 2.1 🤖"


def en_support(*args) -> str:
    return \
        f"In case of errors or any problems with the bot, please write to support: @diominvdev.\n\nThe current version of the bot is 2.1 🤖"


s: dict = {
    "support": {
        "ru": ru_support,
        "en": en_support
    }
}
