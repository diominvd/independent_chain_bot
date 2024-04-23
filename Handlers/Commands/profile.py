from aiogram import F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery

from config import bot, dispatcher, database as db
from Keyboards.Inline import main_keyboard
import Parse as parse
import Text as txt


@dispatcher.message(Command("profile"))
async def profile(message: Message) -> None:
    # Update last user activity.
    db.update_last_activity(user_id=message.from_user.id)
    # Load user language.
    user_language: str = db.get_user_language(user_id=message.from_user.id)
    # Delete message with /profile command.
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    # Send main message with keyboard.
    await bot.send_message(
        chat_id=message.from_user.id,
        text=txt.translate_text(s, "profile", user_language, message.from_user.id),
        reply_markup=main_keyboard(user_id=message.from_user.id, language=user_language))
    return None


@dispatcher.callback_query(F.data == "profile")
async def profile_call(callback: CallbackQuery) -> None:
    # Stop callback.
    await callback.answer(show_alert=False)
    # Update last user activity.
    db.update_last_activity(user_id=callback.from_user.id)
    # Load user language.
    user_language: str = db.get_user_language(user_id=callback.from_user.id)
    # Edit main message.
    await bot.edit_message_text(
        text=txt.translate_text(s, "profile", user_language, callback.from_user.id),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id)
    # Add keyboard to message.
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=main_keyboard(user_id=callback.from_user.id, language=user_language))
    return None


def ru_profile(user_id: int) -> str:
    profile_data: list = db.load_profile_data(user_id)
    profile_data[4] = "Не привязан" if profile_data[4] is None else profile_data[4]
    return \
        f"{parse.bold('Привет,')} @{profile_data[0]} 👋\n{parse.bold('Ваш UID')}: {profile_data[1]}\n{parse.bold('Баланс')}: {profile_data[2]} $tINCH\n{parse.bold('Друзья')}: {profile_data[3]}\n{parse.bold('Ton Space')}: {parse.code(profile_data[4])}"


def en_profile(user_id: int) -> str:
    profile_data: list = db.load_profile_data(user_id)
    profile_data[4] = "Not linked" if profile_data[4] is None else profile_data[4]
    return f"{parse.bold('User')} @{profile_data[0]} 👋\n{parse.bold('Your UID')}: {profile_data[1]}\n{parse.bold('Balance')}: {profile_data[2]} $tINCH\n{parse.bold('Friends')}: {profile_data[3]}\n{parse.bold('Ton Space')}: {parse.code(profile_data[4])}"


s: dict = {
    "profile": {
        "ru": ru_profile,
        "en": en_profile
    }
}
