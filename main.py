import asyncio
import logging
from aiogram.methods import DeleteWebhook

from config import bot, dispatcher
from handlers.command import start, profile
from handlers.callback import check_subscribe, profile, information


logging.basicConfig(level=logging.INFO)


async def main() -> None:
    _bot = asyncio.create_task(bot(DeleteWebhook(drop_pending_updates=True)))
    _dispatcher = asyncio.create_task(dispatcher.start_polling(bot))
    await asyncio.gather(_bot, _dispatcher)


if __name__ == "__main__":
    while True:
        asyncio.run(main())