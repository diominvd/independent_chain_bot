import asyncio

from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import database, bot
from handlers.command import command_router
from middlewares.send_profile import send_profile
from states import BotStates
from utils.translator import translate


@command_router.message(StateFilter(BotStates.waiting_wallet))
@database.update_activity
async def profile_command(message: Message, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "wallet_accepted": {
            "ru": f"Адрес кошелька успешно привязан 🔗",
            "en": f"The wallet address has been successfully linked 🔗"
        }
    }

    request_message_id: int = message.message_id
    wallet_address: str = message.text
    database.update_wallet(user_id=message.from_user.id, wallet=wallet_address)

    await bot.delete_message(chat_id=message.chat.id, message_id=request_message_id)
    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=request_message_id - 1,
        text=translate(message, strings["wallet_accepted"])
    )

    await asyncio.sleep(3)

    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=request_message_id - 1,
    )
    await state.clear()
    await send_profile(message)
    return None
