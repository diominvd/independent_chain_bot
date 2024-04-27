import asyncio
from aiogram.methods import DeleteWebhook
import logging

from config import bot, dispatcher

# Handlers. Comment for off.
from Handlers.Admin import command
from Handlers.Events import callback
from Handlers.Information import callback
from Handlers.Profile import callback, command
from Handlers.Send import command
from Handlers.Start import command
from Handlers.Subscribe import callback
from Handlers.Support import callback
from Handlers.Wallet import callback, message

# Comment down string for off logging.
logging.basicConfig(level=logging.INFO)


async def main() -> None:
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    while True:
        asyncio.run(main())