import asyncio
from aiogram.methods import DeleteWebhook
import logging

from config import bot, dispatcher

# Handlers. Comment for off.
import Handlers.Commands.admin
import Handlers.Commands.events
import Handlers.Commands.information
import Handlers.Commands.profile
import Handlers.Commands.start
import Handlers.Commands.support
import Handlers.Commands.wallet

# Comment down string for off logging.
logging.basicConfig(level=logging.INFO)


async def main() -> None:
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    while True:
        asyncio.run(main())