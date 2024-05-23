import datetime

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database import t_users, t_users_codes
from modules.main import MainModule
from states import CodesStates
from utils import Translator


def format_time(callback: CallbackQuery, time: datetime) -> str:
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

    language: str = t_users.select(("language", ), "user_id", callback.from_user.id)
    seconds: float = 86400 - time
    hours = int(seconds // 3600)
    minutes = (seconds % 3600) // 60

    if hours == 1:
        hours_str = f"1 {strings['hour'][language][0]}"
    elif 2 <= hours <= 4:
        hours_str = f"{hours} {strings['hour'][language][1]}"
    elif 21 <= hours <= 24:
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


@MainModule.router.callback_query(F.data == "codes")
async def h_codes(callback: CallbackQuery, state: FSMContext):

    user = t_users_codes.user(callback.from_user.id)
    time_difference: float = (datetime.datetime.now() - user.last_code).total_seconds()

    if time_difference < 86400:
        strings: dict[str, dict] = {
            "limit": {
                "ru": f"Следующая активация будет доступна через\n{format_time(callback, time_difference)}",
                "en": f"Next activation will be available via\n{format_time(callback, time_difference)}"
            }
        }

        await callback.answer(
            text=Translator.text(callback, strings, "limit"),
            show_alert=True
        )

        return None
    else:
        strings: dict[str, dict] = {
            "codes": {
                "ru": f"Отправьте 16-ти значный код для его активации 🔠",
                "en": f"Send a 16-digit code to activate it 🔠"
            }
        }

        await callback.answer(show_alert=False)
        await state.set_state(CodesStates.code)
        await state.update_data(anchor=callback.message.message_id)

        user: tuple = t_users_codes.select(("user_id",), "user_id", callback.from_user.id)
        if user is None:
            t_users_codes.insert(
                user_id=callback.from_user.id,
                username=callback.from_user.username,
                last_code=datetime.datetime.now() - datetime.timedelta(days=1),
            )

        await callback.message.edit_text(
            text=Translator.text(callback, strings, "codes"),
            reply_markup=MainModule.modules["codes"].keyboard(callback, "back")
        )