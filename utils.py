import asyncio
from aiogram.types import Message, CallbackQuery
from datetime import datetime

from config import bot


def translate_text(strings: dict, key: str, language: str, *args) -> str:
    language = "en" if language not in ["ru", "en"] else language
    return strings[key][language](*args)


def translate_button(strings: dict, key: str, language: str) -> str:
    language = "en" if language not in ["ru", "en"] else language
    return strings[key][language]


def pack_user_data(message: Message) -> dict:
    user_data: dict = {
        "registration": str(datetime.now().strftime("%d.%m.%Y %H:%M:%S")),
        "last_activity": str(datetime.now().strftime("%d.%m.%Y %H:%M:%S")),
        "language": str(message.from_user.language_code),
        "telegram_id": int(message.from_user.id),
        "username": str(message.from_user.username),
        "balance": 100,
        "referals": 0,
    }
    return user_data


def fetch_inviter_id(message: Message) -> int:
    user_id: int = int(message.from_user.id)
    message_data: list = message.text.split(" ")
    if len(message_data) > 1:
        if message_data[1] == user_id:
            inviter_id: int = 0
        else:
            inviter_id: int = message_data[1]
    else:
        inviter_id = 0
    return inviter_id


async def check_subscribe(_obj: Message | CallbackQuery) -> bool:
    subscribe: bool = False
    user_status = await bot.get_chat_member(chat_id="@inch_coin", user_id=_obj.from_user.id)
    if user_status.status.split(".")[0] in ["member", "administrator", "creator"]:
        subscribe = True
    else:
        subscribe = False
    user_status = await bot.get_chat_member(chat_id="@inch_coin", user_id=_obj.from_user.id)
    if user_status.status.split(".")[0] in ["member", "administrator", "creator"]:
        subscribe = True
    else:
        subscribe = False
    return subscribe
