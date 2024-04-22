import asyncio
import logging
from aiogram.methods import DeleteWebhook

from config import bot, dispatcher
import Handlers


logging.basicConfig(level=logging.INFO)


async def main() -> None:
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    while True:
        asyncio.run(main())