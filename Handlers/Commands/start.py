from aiogram import F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import bot, dispatcher, database as db
from Keyboards.Inline import check_subscribe_keyboard
import Parse as parse
from States.Default import DefaultStates
import Text as txt
import utils as u


@dispatcher.message(Command("start"))
async def start(message: Message, state: FSMContext) -> None:
    # Update last user activity.
    db.update_last_activity(user_id=message.from_user.id)
    # Check user existence in database.
    if not db.check_user_existence(message.from_user.id):
        db.add_new_user(user_data=u.pack_user_data(message))
        db.check_user_inviter(user_id=message.from_user.id,
                              inviter_id=u.get_inviter_id(message))
    # Load user language.
    user_language: str = db.get_user_language(user_id=message.from_user.id)
    # Check user subscribe on channels.
    if not await u.check_subscribe(user_id=message.from_user.id):
        # Send message with channels.
        await message.answer(
            text=txt.translate_text(s, "alert", user_language),
            reply_markup=check_subscribe_keyboard(language=user_language))
        # Set state for check callback from check button.
        await state.set_state(DefaultStates.check_subscribe)
    else:
        # Delete message with /start command.
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
        # Send start message
        await bot.send_message(
            chat_id=message.from_user.id,
            text=txt.translate_text(s, "start", user_language))
    return None


@dispatcher.callback_query(F.data == "check_subscribe", StateFilter(DefaultStates.check_subscribe))
async def subscribe_callback(callback: CallbackQuery, state: FSMContext) -> None:
    # Load user language.
    user_language: str = db.get_user_language(user_id=callback.from_user.id)
    # Check user subscribe on channels.
    if not await u.check_subscribe(user_id=callback.from_user.id):
        await callback.answer(
            text=txt.translate_text(s, "check_error", user_language))
    else:
        await callback.answer(
            text=txt.translate_text(s, "check_success", user_language))
        # Delete /start message and message with channels.
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id - 1)
        # Send start message.
        await bot.send_message(
            chat_id=callback.from_user.id, text=txt.translate_text(s, "start", user_language))
        # Clear states.
        await state.clear()
    return None


def ru_alert(*args) -> str:
    return "Для использования бота подпишитесь на каналы проекта. После этого нажмите кнопку \"Проверить\"."


def en_alert(*args) -> str:
    return "To use the bot, subscribe to the project channels. After that, click \"Check\"."


def ru_check_error(*args) -> str:
    return "Проверка не пройдена."


def en_check_error(*args) -> str:
    return "The check is not passed."


def ru_check_success(*args) -> str:
    return "Проверка пройдена."


def en_check_success(*args) -> str:
    return "The check is passed."


def ru_start(*args) -> str:
    return \
        f"Добро пожаловать в {parse.bold('Independent Chain')} - амбициозный проект, с грандиозными планами. Этот бот поможет вам присоединиться к нашему сообществу и оставаться в курсе последних новостей. Получите {parse.bold('100')} $tINCH за подписку на каналы проекта и начинайте приглашать друзей 🤑 Ведь только вместе мы сможем добиться успеха. Получайте {parse.bold('50')} $tINCH за каждого приглашённого друга 💸\n\nДля просмотра профиля воспользуйтесь командой /profile. Для того, чтобы привязать свой Ton Space кошелёк воспользуйтесь кнопкой \"Кошелёк\"."


def en_start(*args) -> str:
    return \
        f"Welcome to the {parse.bold('Independent Chain')}, an ambitious project with ambitious plans. This bot will help you join our community and stay up to date with the latest news. Get {parse.bold('100')} $tINCH for subscribing to the project channels and start inviting friends 🤑 After all, only together we can succeed. Get {parse.bold('50')} $tINCH for each invited friend 💸\n\nTo view the profile, use the /profile command. In order to link your Ton Space wallet, use the \"Wallet\" button."


s: dict = {
    "alert": {
        "ru": ru_alert,
        "en": en_alert
    },
    "check_error": {
        "ru": ru_check_error,
        "en": en_check_error
    },
    "check_success": {
        "ru": ru_check_success,
        "en": en_check_success
    },
    "start": {
        "ru": ru_start,
        "en": en_start
    }
}
