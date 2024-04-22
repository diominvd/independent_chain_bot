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


@dispatcher.message(Command("restart"))
async def start(message: Message, state: FSMContext) -> None:
    if not await u.check_subscribe(message):
        # Send message with channels.
        await message.answer(
            text=u.translate_text(strings, "not_subscribed", database.get_user_language(int(message.from_user.id))),
            reply_markup=check_subscribe_keyboard(database.get_user_language(int(message.from_user.id)))
        )
        # Set state for fetch callback from check button.
        await state.set_state(DefaultStates.check_subscribe_state)
    else:
        database.update_last_activity(int(message.from_user.id))
        await state.clear()
        await bot.send_message(
            chat_id=message.chat.id,
            text=u.translate_text(strings, "restart", database.get_user_language(int(message.from_user.id)))
        )
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)


def ru_restart(*args) -> str:
    text: str = f"Бот перезапущен ♻️"
    return text


def en_restart(*args) -> str:
    text: str = f"Bot restarted ♻️"
    return text


strings: dict = {
    "restart": {
        "ru": ru_restart,
        "en": en_restart
    }
}