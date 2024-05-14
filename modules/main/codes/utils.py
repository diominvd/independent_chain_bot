import datetime

from aiogram.types import CallbackQuery

from core.config import users_table


def calculate_last_code_time(callback: CallbackQuery, time: datetime) -> str:
    strings: dict[str, dict] = {
        "hour": {
            "ru": ["час", "часа", "часов"],
            "en": ["hour", "hours", "hours"]
        },
        "minute": {
            "ru": ["минуту", "минуты", "минут"],
            "en": ["minute", "minutes", "minutes"]
        },
        "back": {
            "ru": "назад",
            "en": "back"
        }
    }

    language: str = users_table.get_value("language", "user_id", callback.from_user.id)
    seconds: float = 86400 - time
    hours = int(seconds // 3600)
    minutes = (seconds % 3600) // 60

    if hours == 1:
        hours_str = f"1 {strings['hour'][language][0]}"
    elif 2 <= hours <= 4:
        hours_str = f"{hours} {strings['hour'][language][1]}"
    else:
        hours_str = f"{hours} {strings['hour'][language][2]}"

    if minutes == 1:
        minutes_str = f"1 {strings['minute'][language][0]}"
    elif 2 <= minutes <= 4:
        minutes_str = f"{int(minutes)} {strings['minute'][language][1]}"
    else:
        minutes_str = f"{int(minutes)} {strings['minute'][language][2]}"

    if hours == 0:
        return f"{minutes_str}"
    else:
        return f"{hours_str} {minutes_str}"