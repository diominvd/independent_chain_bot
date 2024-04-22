from aiogram.filters import Command
from aiogram.types import Message

from config import bot, dispatcher


@dispatcher.message(Command("start"))
async def start(message: Message) -> None:
    pass