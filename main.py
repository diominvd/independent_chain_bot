import logging
import asyncio

from config import dispatcher, bot
import Handlers

logging.basicConfig(level=logging.INFO)


async def main():
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
