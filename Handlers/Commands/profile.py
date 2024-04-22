from aiogram import F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from Keyboards.Inline import main_keyboard
import Parse as p
from config import bot, dispatcher, database
from States.Default import DefaultStates
import utils as u


@dispatcher.message(Command("profile"))
async def profile(message: Message, state: FSMContext):
    database.update_last_activity(int(message.from_user.id))
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=u.translate_text(strings, "profile_message", database.get_user_language(int(message.from_user.id)), int(message.from_user.id)),
        reply_markup=main_keyboard(database.get_user_language(int(message.from_user.id)))
    )


@dispatcher.callback_query(F.data == "profile")
async def profile_call(callback: CallbackQuery, state: FSMContext):
    database.update_last_activity(int(callback.from_user.id))
    await bot.edit_message_text(
        text=u.translate_text(strings, "profile_message", database.get_user_language(int(callback.from_user.id)), int(callback.from_user.id)),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id
    )
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=main_keyboard(database.get_user_language(int(callback.from_user.id)))
    )


def ru_profile(user_id: int) -> str:
    profile_data: list = database.load_profile_data(user_id)
    if profile_data[4] is None:
        profile_data[4] = "Не привязан"
    text: str = f"""{p.bold("👤 Пользователь")} @{profile_data[0]}\n{p.bold("🆔 Идентификатор")}: {profile_data[1]}\n{p.bold("🤑 Баланс")}: {profile_data[2]} $tINCH\n{p.bold("🤝 Ваши рефералы")}: {profile_data[3]}\n{p.bold("👛 Ton Space")}: {p.code(profile_data[4])}\n\n{p.bold("🔗 Реферальная ссылка")}: {p.code(f"t.me/inch_coin_bot?start={user_id}")}\n(Нажмите чтобы скопировать)"""
    return text


def en_profile(user_id: int) -> str:
    profile_data: list = database.load_profile_data(user_id)
    if profile_data[4] is None:
        profile_data[4] = "Not linked"
    text: str = f"""{p.bold("👤 User")} @{profile_data[0]}\n{p.bold("🆔 Identifier")}: {profile_data[1]}\n{p.bold("🤑 Balance")}: {profile_data[2]} $tINCH\n{p.bold("🤝 Your referals")}: {profile_data[3]}\n{p.bold("👛 Ton Space")}: {p.code(profile_data[4])}\n\n{p.bold("🔗 Referral link")}: {p.code(f"t.me/inch_coin_bot?start={user_id}")}\n(Click to copy)"""
    return text


strings: dict = {
    "profile_message": {
        "ru": ru_profile,
        "en": en_profile
    }
}