import datetime

from aiogram.types import Message

from core.config import users_table


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
        "language": message.from_user.language_code if message.from_user.language_code in ["ru", "en"] else "en",
        "user_id": message.from_user.id,
        "inviter_id": check_inviter(message),
        "username": message.from_user.username,
        "balance": users_table.start_reward,
        "referals": 0,
        "codes": 0,
        "last_code_activate": datetime.datetime.now() - datetime.timedelta(days=1),
    }
    return user_data