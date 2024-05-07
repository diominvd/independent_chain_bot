from aiogram.filters import Command
from aiogram.types import Message

from modules.main import MainModule
from core.config import users_table
from markdown import Markdown
from utils import translate


@MainModule.router.message(Command("panel"))
async def start(message: Message) -> None:
    pass