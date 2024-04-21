from aiogram.types import Message

import Keyboards
import strings
from config import bot


def fetch_user_id(message: Message) -> int:
    return message.chat.id


def fetch_username(message: Message) -> str:
    return message.chat.username


def fetch_registration_date(message: Message) -> str:
    return str(message.date.date())


def fetch_user_language(message: Message) -> str:
    return message.from_user.language_code


def fetch_inviter_id(message: Message) -> int:
    try:
        inviter_id: int = int(message.text.split(" ")[1])
        if inviter_id == fetch_user_id(message):
            inviter_id: int = 0
    except IndexError:
        inviter_id: int = 0
    return inviter_id


def fetch_message_text(message: Message) -> str:
    try:
        message_text: str = message.text.split(" ")[0]
    except IndexError:
        message_text: str = message.text
    return message_text


async def subscribe_check(message: Message):
    user_language: str = fetch_user_language(message)
    keyboard = Keyboards.start_keyboard(user_language)
    channel_member = await bot.get_chat_member(chat_id="@inch_coin", user_id=message.chat.id)
    status = channel_member.status.split(".")[0]
    if status in ["member", "administrator", "creator"]:
        channel_member = await bot.get_chat_member(chat_id="@diominvdev", user_id=message.chat.id)
        status = channel_member.status.split(".")[0]
        if status in ["member", "creator"]:
            return True
        else:
            return False
    else:
        return False
