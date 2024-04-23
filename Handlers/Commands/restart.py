from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import bot, dispatcher, database as db
from Keyboards.Inline import check_subscribe_keyboard
from States.Default import DefaultStates
import Text as txt
import utils as u


@dispatcher.message(Command("restart"))
async def start(message: Message, state: FSMContext) -> None:
    # Update last user activity.
    db.update_last_activity(user_id=message.from_user.id)
    # Load user language.
    user_language: str = db.get_user_language(user_id=message.from_user.id)
    # Check subscribe.
    if not await u.check_subscribe(user_id=message.from_user.id):
        # Send message with channels.
        await message.answer(
            text=txt.translate_text(s, "not_subscribed", user_language),
            reply_markup=check_subscribe_keyboard(user_language))
        # Set state for fetch callback from check button.
        await state.set_state(DefaultStates.check_subscribe)
    else:
        # Clear all states.
        await state.clear()
        await bot.send_message(
            chat_id=message.chat.id,
            text=txt.translate_text(s, "restart", user_language))
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    return None


def ru_restart(*args) -> str:
    return \
        f"Бот перезапущен ♻️. Воспользуйтесь командой /start."


def en_restart(*args) -> str:
    return \
        f"Bot restarted ♻️ Use command /start."


s: dict = {
    "restart": {
        "ru": ru_restart,
        "en": en_restart
    }
}
