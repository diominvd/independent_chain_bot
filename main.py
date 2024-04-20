import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from config import API_KEY


logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_KEY)
dispatcher = Dispatcher()


async def start() -> None:
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start())