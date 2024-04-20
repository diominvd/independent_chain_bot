from aiogram.filters import Command
from aiogram.types import Message

from config import dispatcher, database
from strings import translate_answer
import utils as u


@dispatcher.message(Command("start"))
async def start_handler(message: Message) -> None:
    telegram_id: int = u.fetch_user_id(message)
    username: str = u.fetch_username(message)
    user_language: str = u.fetch_user_language(message)
    registration_date: str = u.fetch_registration_date(message)
    inviter_id: int = u.fetch_inviter_id(message)
    message_text: str = u.fetch_message_text(message)
    # Check user in database.
    if not database.check_user(telegram_id):
        database.create_user(telegram_id, username, user_language, registration_date, inviter_id)
    # Answer with correct language.
    answer_text: str = translate_answer(message_text, user_language)
    await message.answer(answer_text)


@dispatcher.message(Command("info"))
async def profile_handler(message: Message) -> None:
    user_language = u.fetch_user_language(message)
    answer_text: str = translate_answer(message.text, user_language)
    await message.answer(answer_text)


@dispatcher.message(Command("profile"))
async def profile_handler(message: Message) -> None:
    user_id: int = u.fetch_user_id(message)
    user_language = u.fetch_user_language(message)
    profile_data = database.load_profile(user_id)
    answer_text: str = translate_answer(message.text, user_language, profile_data)
    await message.answer(answer_text)


@dispatcher.message(Command("links"))
async def profile_handler(message: Message) -> None:
    user_language = u.fetch_user_language(message)
    answer_text: str = translate_answer(message.text, user_language)
    await message.answer(answer_text)


@dispatcher.message(Command("coin"))
async def profile_handler(message: Message) -> None:
    user_language = u.fetch_user_language(message)
    answer_text: str = translate_answer(message.text, user_language)
    await message.answer(answer_text)
