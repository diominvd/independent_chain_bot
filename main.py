import asyncio
import logging
from aiogram.methods import DeleteWebhook

from core.config import bot, dispatcher
from modules.main import MainModule
from modules.group import GroupModule
from modules.admin import AdminModule

# Comment down string for off logging.
logging.basicConfig(level=logging.INFO)

dispatcher.include_routers(MainModule.router, GroupModule.router, AdminModule.router)


async def main() -> None:
    bot_task = asyncio.create_task(bot.delete_webhook(drop_pending_updates=True))
    dispatcher_task = asyncio.create_task(dispatcher.start_polling(bot))
    #storage_checker_task = asyncio.create_task(MainModule.modules["mining"].storage_checker(bot))

    await bot_task
    await dispatcher_task
    #await storage_checker_task


if __name__ == "__main__":
    while True:
        asyncio.run(main())