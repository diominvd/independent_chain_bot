from aiogram.filters import Command
from aiogram.types import Message

from config import dispatcher
from strings import translate_answer


@dispatcher.message(Command("start"))
async def start_handler(message: Message) -> None:
    # user_language: str = ... вытаскивать язык пользователя из БД.
    user_language = "Заглушка"
    answer_text: str = translate_answer(message.text, user_language)
    await message.answer(answer_text)


@dispatcher.message(Command("info"))
async def profile_handler(message: Message) -> None:
    # user_language: str = ... вытаскивать язык пользователя из БД.
    user_language = "Заглушка"
    answer_text: str = translate_answer(message.text, user_language)
    await message.answer(answer_text)


@dispatcher.message(Command("profile"))
async def profile_handler(message: Message) -> None:
    # user_language: str = ... вытаскивать язык пользователя из БД.
    user_language = "Заглушка"
    answer_text: str = translate_answer(message.text, user_language)
    await message.answer(answer_text)


@dispatcher.message(Command("links"))
async def profile_handler(message: Message) -> None:
    # user_language: str = ... вытаскивать язык пользователя из БД.
    user_language = "Заглушка"
    answer_text: str = translate_answer(message.text, user_language)
    await message.answer(answer_text)


@dispatcher.message(Command("settings"))
async def profile_handler(message: Message) -> None:
    # user_language: str = ... вытаскивать язык пользователя из БД.
    user_language = "Заглушка"
    answer_text: str = translate_answer(message.text, user_language)
    await message.answer(answer_text)