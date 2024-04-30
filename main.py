import asyncio
import logging
from aiogram.methods import DeleteWebhook

from config import bot, dispatcher

from handlers.command import start, profile
from handlers.callback import check_subscribe, profile, information, support, wallet, events
from handlers.message import wallet_address
# Admin imports.
from administration.handlers.command import admin
from administration.handlers.callback import admin, admin_exit, mail, mailing, statistic
from administration.handlers.message import mailing_text, mail_text
# Events imports.
from handlers.events import raffle_nft
from handlers.events.raffle_nft import timer

# Comment on for disable logging.
logging.basicConfig(level=logging.INFO)


async def main() -> None:
    _bot = asyncio.create_task(bot(DeleteWebhook(drop_pending_updates=True)))
    _dispatcher = asyncio.create_task(dispatcher.start_polling(bot))
    _timer = asyncio.create_task(timer())
    await asyncio.gather(_bot, _dispatcher, _timer)


if __name__ == "__main__":
    while True:
        asyncio.run(main())