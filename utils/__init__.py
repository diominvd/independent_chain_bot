import datetime

from aiogram.types import Message, CallbackQuery

from core.config import users_table


def translate(event: Message | CallbackQuery, strings: dict, key: str) -> str:
    user_language: str = users_table.get_value("language", "user_id", event.from_user.id)
    return strings[key][user_language]


def check_inviter(message: Message) -> int:
    try:
        inviter_id: int = int(message.text.split(" ")[1])
    except IndexError:
        return 0
    else:
        if inviter_id != message.from_user.id:
            return inviter_id
        else:
            return 0


def pack_user_data(message: Message) -> dict:
    user_data: dict[str, any] = {
        "registration": datetime.datetime.now(),
        "last_activity": datetime.datetime.now(),
        "language": message.from_user.language_code,
        "user_id": message.from_user.id,
        "inviter_id": check_inviter(message),
        "username": message.from_user.username,
        "balance": 100,
        "referals": 0
    }
    return user_data