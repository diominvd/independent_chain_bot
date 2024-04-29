from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import database
from handlers.command import command_router
from middlewares.send_profile import send_profile


@command_router.message(Command("profile"))
@database.update_activity
async def profile_command(message: Message, state: FSMContext) -> None:
    language: str = database.get_user_language(user_id=message.from_user.id)
    await send_profile(message, language)
    return None
