from aiogram import F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from Handlers.Commands.profile import profile
from Keyboards.Inline import check_subscribe_keyboard
import Parse as p
from config import bot, dispatcher, database
from States.Default import DefaultStates
import utils as u


@dispatcher.message(Command("start"))
async def start(message: Message, state: FSMContext) -> None:
    await state.clear()
    database.update_last_activity(int(message.from_user.id))
    if not database.check_user_existence(int(message.from_user.id)):
        database.add_new_user(u.pack_user_data(message))
        database.check_user_inviter(int(message.from_user.id), u.fetch_inviter_id(message))
    if not await u.check_subscribe(message):
        # Send message with channels.
        await message.answer(
            text=u.translate_text(strings, "not_subscribed", database.get_user_language(int(message.from_user.id))),
            reply_markup=check_subscribe_keyboard(database.get_user_language(int(message.from_user.id)))
        )
        # Set state for fetch callback from check button.
        await state.set_state(DefaultStates.check_subscribe_state)
    else:
        await state.clear()
        # Delete /start message.
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
        # Send start message
        await bot.send_message(
            chat_id=message.from_user.id,
            text=u.translate_text(strings, "start_message", database.get_user_language(int(message.from_user.id)))
        )


@dispatcher.callback_query(F.data == "check_subscribe", StateFilter(DefaultStates.check_subscribe_state))
async def subscribe_callback(callback: CallbackQuery, state: FSMContext) -> None:
    if not await u.check_subscribe(callback):
        await callback.answer(
            text=u.translate_text(strings, "callback_error", database.get_user_language(int(callback.from_user.id))))
    else:
        await callback.answer(
            text=u.translate_text(strings, "callback_success", database.get_user_language(int(callback.from_user.id))))
        # Delete /start message and message with channels.
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id - 1)
        # Clear states.
        await state.clear()
        # Send start message
        await bot.send_message(
            chat_id=callback.from_user.id, text=u.translate_text(strings, "start_message", database.get_user_language(int(callback.from_user.id)))
        )


def ru_not_subscribed(*args) -> str:
    return "Для использования бота подпишитесь на каналы проекта. После этого нажмите кнопку \"Проверить\"."


def en_not_subscribed(*args) -> str:
    return "To use the bot, subscribe to the project channels. After that, click \"Check\"."


def ru_callback_error(*args) -> str:
    return "Вы не подписаны на каналы."


def en_callback_error(*args) -> str:
    return "You are not subscribed to channels."


def ru_callback_success(*args) -> str:
    return "Проверка пройдена."


def en_callback_success(*args) -> str:
    return "The check is passed."


def ru_start_message(*args) -> str:
    text: str = f"""Добро пожаловать в {p.bold("Independent Chain")} - амбициозный проект, с грандиозными планами. Этот бот поможет вам присоединиться к нашему сообществу и оставаться в курсе последних новостей. Получите {p.bold("100")} $tINCH за подписку на каналы проекта и начинайте приглашать друзей 🤑 Ведь только вместе мы сможем добиться успеха. Получайте {p.bold("50")} $tINCH за каждого приглашённого друга 💸\n\nДля просмотра профиля воспользуйтесь командой /profile. Для того, чтобы привязать свой Ton Space кошелёк воспользуйтесь кнопкой \"Кошелёк\"."""
    return text


def en_start_message(*args) -> str:
    text: str = f"""Welcome to the {p.bold("Independent Chain")}, an ambitious project with ambitious plans. This bot will help you join our community and stay up to date with the latest news. Get {p.bold("100")} $tINCH for subscribing to the project channels and start inviting friends 🤑 After all, only together we can succeed. Get {p.bold("50")} $tINCH for each invited friend 💸\n\nTo view the profile, use the /profile command. In order to link your Ton Space wallet, use the \"Wallet\" button."""
    return text


strings: dict = {
    "not_subscribed": {
        "ru": ru_not_subscribed,
        "en": en_not_subscribed
    },
    "callback_error": {
        "ru": ru_callback_error,
        "en": en_callback_error
    },
    "callback_success": {
        "ru": ru_callback_success,
        "en": en_callback_success
    },
    "start_message": {
        "ru": ru_start_message,
        "en": en_start_message
    }
}
