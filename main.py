import asyncio
import logging
from aiogram.methods import DeleteWebhook

from core.config import bot, dispatcher
from modules.main import MainModule
from modules.admin import AdminModule

# Comment down string for off logging.
logging.basicConfig(level=logging.INFO)

dispatcher.include_routers(MainModule.router, AdminModule.router)


async def main() -> None:
    bot_task = asyncio.create_task(bot(DeleteWebhook(drop_pending_updates=True)))
    dispatcher_task = asyncio.create_task(dispatcher.start_polling(bot))
    await asyncio.gather(bot_task, dispatcher_task)


if __name__ == "__main__":
    while True:
        asyncio.run(main())