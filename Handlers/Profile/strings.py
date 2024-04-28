from config import database as db
from markdown import Markdown


def ru_profile(user_id: int) -> str:
    profile_data: list = db.load_profile_data(user_id)
    profile_data[4] = "Не привязан" if profile_data[4] is None else profile_data[4]
    return (f"{Markdown.bold('Привет,')} @{profile_data[0]} 👋\n"
            f"{Markdown.bold('Ваш UID')}: {profile_data[1]}\n"
            f"{Markdown.bold('Баланс')}: {profile_data[2]} $tINCH\n"
            f"{Markdown.bold('Друзья')}: {profile_data[3]}\n"
            f"{Markdown.bold('Ton Space')}: {Markdown.code(profile_data[4])}\n\n"
            f"{Markdown.bold('Реферальная ссылка')}:\n"
            f"{Markdown.code(f't.me/inch_coin_bot?start={user_id}')}\n"
            f"(Нажмите, чтобы скопировать)")


def en_profile(user_id: int) -> str:
    profile_data: list = db.load_profile_data(user_id)
    profile_data[4] = "Not linked" if profile_data[4] is None else profile_data[4]
    return (f"{Markdown.bold('Hello,')} @{profile_data[0]} 👋\n"
            f"{Markdown.bold('Your UID')}: {profile_data[1]}\n"
            f"{Markdown.bold('Balance')}: {profile_data[2]} $tINCH\n"
            f"{Markdown.bold('Friends')}: {profile_data[3]}\n"
            f"{Markdown.bold('Ton Space')}: {Markdown.code(profile_data[4])}\n\n"
            f"{Markdown.bold('Referal link')}:\n"
            f"{Markdown.code(f't.me/inch_coin_bot?start={user_id}')}\n"
            f"(Click to copy)")


def ru_alert(*args) -> str:
    return "Данные обновлены."


def en_alert(*args) -> str:
    return "The data has been updated."


strings: dict = {
    "profile": {
        "ru": ru_profile,
        "en": en_profile
    },
    "alert": {
        "ru": ru_alert,
        "en": en_alert
    }
}