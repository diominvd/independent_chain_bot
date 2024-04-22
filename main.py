import asyncio
import logging

from config import bot, dispatcher
import Handlers


logging.basicConfig(level=logging.INFO)


async def main() -> None:
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    while True:
        asyncio.run(main())