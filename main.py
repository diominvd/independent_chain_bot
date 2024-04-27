import asyncio
from aiogram.methods import DeleteWebhook
import logging

from config import bot, dispatcher
from Handlers.Events.callback import send_top

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
    bot_task = asyncio.create_task(bot(DeleteWebhook(drop_pending_updates=True)))
    dispatcher_task = asyncio.create_task(dispatcher.start_polling(bot))
    timer = asyncio.create_task(send_top())
    await asyncio.gather(bot_task, dispatcher_task, timer)


if __name__ == "__main__":
    while True:
        asyncio.run(main())
