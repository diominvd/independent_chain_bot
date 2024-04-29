from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import database
from config import event_database
from handlers.command import command_router
from middlewares.check_subscribe import check_subscribe
from middlewares.send_greeting import send_greeting
from utils.pack_user_data import pack_user_data


@command_router.message(Command("start"))
@database.update_activity
async def start_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    # Verification of the user's existence.
    if database.check_user(user_id=message.from_user.id) is False:
        user_data: dict = pack_user_data(event=message)
        database.create_user(user_data)
        # Event function.
        event_database.update_participant(message)
    # Load user language.
    language: str = database.get_user_language(user_id=message.from_user.id)
    # Check subscribe in channel.
    if await check_subscribe(message):
        await send_greeting(message)
    return None
