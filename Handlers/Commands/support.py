from aiogram import F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from Keyboards.Inline import main_keyboard
import Parse as p
from config import bot, dispatcher, database
from States.Default import DefaultStates
import utils as u


@dispatcher.callback_query(F.data == "support")
async def support(callback: CallbackQuery, state: FSMContext):
    database.update_last_activity(int(callback.from_user.id))
    await bot.edit_message_text(
        text=u.translate_text(strings, "support", database.get_user_language(int(callback.from_user.id)), int(callback.from_user.id)),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id
    )
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=main_keyboard(database.get_user_language(int(callback.from_user.id)))
    )


def ru_support(*args) -> str:
    text: str = f"""В случае возникновения ошибок или каких-либо проблем с ботом просим написать вас в поддержку: @diominvdev.\n\nТекущая версия бота 2.0 🤖"""
    return text


def en_support(*args) -> str:
    text: str = f"""In case of errors or any problems with the bot, please write to support: @diominvdev.\n\nThe current version of the bot is 2.0 🤖"""
    return text


strings: dict = {
    "support": {
        "ru": ru_support,
        "en": en_support
    }
}