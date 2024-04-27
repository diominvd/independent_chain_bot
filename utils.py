from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from datetime import datetime

from config import bot, database as db


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


def get_inviter_id(message: Message) -> int:
    user_id: int = int(message.from_user.id)
    message_text: list = message.text.split(" ")
    if len(message_text) > 1:
        if message_text[1] == user_id:
            inviter_id: int = 0
        else:
            inviter_id: int = message_text[1]
    else:
        inviter_id = 0
    return inviter_id


async def check_subscribe(user_id: int, language: str) -> bool:
    subscribe: bool = False
    if language == "ru":
        user_status = await bot.get_chat_member(chat_id="@inch_ru", user_id=user_id)
        if user_status.status.split(".")[0] in ["member", "administrator", "creator"]:
            subscribe = True
        else:
            subscribe = False
    elif language != "ru":
        user_status = await bot.get_chat_member(chat_id="@inch_en", user_id=user_id)
        if user_status.status.split(".")[0] in ["member", "administrator", "creator"]:
            subscribe = True
        else:
            subscribe = False
    return subscribe


def update_last_activity(func):
    async def wrapper(event: Message | CallbackQuery, state: FSMContext):
        db.update_last_activity(user_id=event.from_user.id)
        return await func(event, state)
    return wrapper