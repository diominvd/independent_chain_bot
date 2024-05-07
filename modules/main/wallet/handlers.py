import asyncio

from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from pytonconnect import TonConnect
from pytoniq_core import Address

from modules.main import MainModule
from markdown import Markdown
from core.config import users_table
from utils import translate


@MainModule.router.callback_query(F.data == "wallet")
async def wallet(callback: CallbackQuery) -> None:
    strings: dict[str, dict] = {
        "information": {
            "ru": "Подключите ваш кошелёк Ton Space в течении трёх минут 💳",
            "en": "Connect your Ton Space wallet within 3 minutes 💳"
        },
        "success": {
            "ru": "Кошелёк успешно подключён!",
            "en": "The wallet has been successfully connected!"
        },
        "failed": {
            "ru": "Время ожидания подключения вышло.",
            "en": "The connection timeout has expired."
        }
    }

    # Generate link for Ton Space connect.
    connector: TonConnect = TonConnect(manifest_url="https://raw.githubusercontent.com/diominvd/independent_chain_bot/main/modules/main/wallet/manifest.json")
    wallets_list: dict = TonConnect.get_wallets()
    connect_url: str = await connector.connect(wallets_list[0])

    await callback.message.edit_text(
        text=translate(callback, strings, "information"),
        reply_markup=MainModule.modules["wallet"].keyboard_connect(callback, connect_url)
    )

    for i in range(1, 180):
        await asyncio.sleep(1)
        if connector.connected:
            if connector.account.address:
                wallet_address = connector.account.address
                wallet_address = Address(wallet_address).to_str(is_bounceable=False)

                # Update user wallet in database.
                users_table.update_wallet(callback.from_user.id, wallet_address)

                await callback.message.edit_text(
                    text=translate(callback, strings, "success"),
                    reply_markup=MainModule.modules["wallet"].keyboard_finish(callback)
                )
                break
    else:
        await callback.message.edit_text(
            text=translate(callback, strings, "failed"),
            reply_markup=MainModule.modules["wallet"].keyboard_finish(callback)
        )
    return None