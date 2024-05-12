from aiogram.types import CallbackQuery
from pytonapi import Tonapi

from core.config import users_table, mining_table
from core.secrets import TON_API
from translator import Translator


async def check_wallet_bind(callback: CallbackQuery) -> bool:
    strings: dict[str, dict] = {
        "check": {
            "ru": "Привяжите кошелёк Ton Space для доступа к функции добыче.",
            "en": "Link a Ton Space wallet to access the mining function."
        }
    }

    address: str | None = users_table.get_value("wallet", "user_id", callback.from_user.id)
    if address is None:
        await callback.answer(
            text=Translator.text(callback, strings, "check"),
            show_alert=True)
        return False


def update_boosters(user_id: int) -> None:
    wallet_address: str = users_table.get_value("wallet", "user_id", user_id)
    ton: Tonapi = Tonapi(api_key=TON_API)
    response = ton.accounts.get_nfts(account_id=wallet_address, limit=100)
    boosters_value: float = 1

    for nft in response.nft_items:
        if nft.metadata["name"] in ["BRONZE INCH", "SILVER INCH", "GOLD INCH", "GECKSOHI INCH", "GECKOSHI INCH"]:
            for attribute in nft.metadata["attributes"]:
                if attribute['trait_type'] == 'multiplier':
                    boosters_value = boosters_value * float(attribute["value"])
    mining_table.update_booster(user_id, boosters_value)
    return