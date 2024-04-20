from aiogram.types import Message


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