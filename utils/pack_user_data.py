from aiogram.types import CallbackQuery, Message
from datetime import datetime


def pack_user_data(event: Message | CallbackQuery):
    try:
        inviter_id: int = int(event.text.split(" ")[1])
    except:
        inviter_id = 0

    # Pack user data for database.
    user_data: dict = {
        "registration": str(datetime.now().strftime("%d.%m.%Y %H:%M:%S")),
        "language": event.from_user.language_code,
        "user_id": event.from_user.id,
        "inviter_id": inviter_id,
        "username": event.from_user.username
    }
    return user_data