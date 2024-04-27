from config import database as db
import Parse as parse


def ru_profile(user_id: int) -> str:
    profile_data: list = db.load_profile_data(user_id)
    profile_data[4] = "Не привязан" if profile_data[4] is None else profile_data[4]
    return \
        f"{parse.bold('Привет,')} @{profile_data[0]} 👋\n{parse.bold('Ваш UID')}: {profile_data[1]}\n{parse.bold('Баланс')}: {profile_data[2]} $tINCH\n{parse.bold('Друзья')}: {profile_data[3]}\n{parse.bold('Ton Space')}: {parse.code(profile_data[4])}\n\n{parse.bold('Реферальная ссылка')}:\n{parse.code(f't.me/inch_coin_bot?start={user_id}')}\n(Нажмите, чтобы скопировать)"


def en_profile(user_id: int) -> str:
    profile_data: list = db.load_profile_data(user_id)
    profile_data[4] = "Not linked" if profile_data[4] is None else profile_data[4]
    return f"{parse.bold('User')} @{profile_data[0]} 👋\n{parse.bold('Your UID')}: {profile_data[1]}\n{parse.bold('Balance')}: {profile_data[2]} $tINCH\n{parse.bold('Friends')}: {profile_data[3]}\n{parse.bold('Ton Space')}: {parse.code(profile_data[4])}\n\n{parse.bold('Referal link')}:\n{parse.code(f't.me/inch_coin_bot?start={user_id}')}\n(Click to copy)"


strings: dict = {
    "profile": {
        "ru": ru_profile,
        "en": en_profile
    }
}