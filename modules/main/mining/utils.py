import asyncio
import datetime

from aiogram.types import CallbackQuery
from pytonapi import Tonapi

from core.config import users_table, mining_table
from core.secrets import TON_API
from translator import Translator


def calculate_last_claim_time(callback: CallbackQuery, time: datetime) -> str:
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
    seconds: datetime = (datetime.datetime.now() - time).total_seconds()
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
        return f"{minutes_str} {strings['back'][language]}"
    else:
        return f"{hours_str} {minutes_str} {strings['back'][language]}"


async def check_wallet_bind(callback: CallbackQuery) -> bool:
    address: str | None = users_table.get_value("wallet", "user_id", callback.from_user.id)
    if address is None:
        return False
    else:
        return True


def update_boosters(user_id: int) -> None:
    wallet_address: str = users_table.get_value("wallet", "user_id", user_id)
    ton: Tonapi = Tonapi(api_key=TON_API)
    response = ton.accounts.get_nfts(account_id=wallet_address, limit=100)
    boosters_value: float = 1

    for nft in response.nft_items:
        if nft.metadata["name"] in ["BRONZE INCH", "SILVER INCH", "GOLD INCH", "BLACK INCH", "GECKOSHI INCH", "GHOSTEX INCH"]:
            for attribute in nft.metadata["attributes"]:
                if attribute['trait_type'] == 'multiplier':
                    boosters_value = boosters_value * float(attribute["value"])
    mining_table.update_booster(user_id, boosters_value)
    return


async def storage_checker(bot) -> None:
    while True:
        query: str = f"SELECT * FROM mining ORDER BY last_claim"
        response: list = mining_table.select(query, ())

        for user in response:
            current_time: datetime = datetime.datetime.now()
            last_claim: datetime = user[1]

            time_difference: float = (current_time - last_claim).total_seconds()
            storage: float = user[3] * 60 * 60

            if time_difference > user[3] * 60 * 60:
                if user[0] not in mining_table.full_storage:
                    mining_table.full_storage.append(user[0])

                    user_language: str = users_table.get_value("language", "user_id", user[0])
                    strings: dict[str, dict] = {
                        "notify": {
                            "ru": "Хранилище заполнено.\nПора собирать добычу 🔥\n\nПерейти в профиль: /profile",
                            "en": "The vault is full.\nIt's time to collect the loot 🔥\n\nGo to Profile: /profile"
                        }
                    }

                    if user_language == "ru":
                        text: str = strings["notify"]["ru"]
                    else:
                        text: str = strings["notify"]["en"]

                    await bot.send_message(
                        chat_id=user[0],
                        text=text
                    )
        await asyncio.sleep(60)