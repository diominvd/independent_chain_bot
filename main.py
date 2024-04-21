import logging
import asyncio

from config import bot, dispatcher
import Handlers


logging.basicConfig(level=logging.INFO)


async def main():
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except:
            asyncio.run(main())
