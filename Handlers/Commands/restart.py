import asyncio
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

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
        # Set state for fetch callback from check button.
        await state.set_state(DefaultStates.check_subscribe)
        # Send message with channels.
        await message.answer(
            text=txt.translate_text(s, "alert", user_language),
            reply_markup=check_subscribe_keyboard(user_language))
    else:
        # Clear all states.
        await state.clear()
        # Clear chat history.
        try:
            chat_id: int = message.from_user.id
            message_id: int = message.message_id
            while True:
                try:
                    await bot.delete_message(chat_id=chat_id, message_id=message_id)
                    await asyncio.sleep(0.5)
                except:
                    pass
                message_id -= 1
        except:
            pass
    return None


def ru_alert(*args) -> str:
    return "Для использования бота подпишитесь на каналы проекта. После этого нажмите кнопку \"Проверить\"."


def en_alert(*args) -> str:
    return "To use the bot, subscribe to the project channels. After that, click \"Check\"."


s: dict = {
    "alert": {
        "ru": ru_alert,
        "en": en_alert
    }
}
