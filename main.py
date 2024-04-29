import asyncio
import logging
from aiogram.methods import DeleteWebhook

from config import bot, dispatcher
from middlewares.send_raffle_nft_rating import timer

from handlers.command import start, profile
from handlers.callback import check_subscribe, profile, information, support, wallet, events, e_raffle_nft
from handlers.message import wallet_address


logging.basicConfig(level=logging.INFO)


async def main() -> None:
    _bot = asyncio.create_task(bot(DeleteWebhook(drop_pending_updates=True)))
    _dispatcher = asyncio.create_task(dispatcher.start_polling(bot))
    _timer = asyncio.create_task(timer())
    await asyncio.gather(_bot, _dispatcher, _timer)


if __name__ == "__main__":
    while True:
        asyncio.run(main())