import asyncio

from aiogram import F
from aiogram.types import CallbackQuery
from pytonconnect import TonConnect
from pytoniq_core import Address

from modules.main import MainModule
from core.config import users_table
from utils import translate


@MainModule.router.callback_query(F.data == "wallet")
async def wallet(callback: CallbackQuery) -> None:
    strings: dict[str, dict] = {
        "information": {
            "ru": "Подключите ваш кошелёк Ton Space с помощью специальной кнопки 🔗",
            "en": "Connect your Ton Space wallet using a special button 🔗"
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

    # Start connect timer.
    time_limit: int = 600
    for second in range(1, time_limit):
        await asyncio.sleep(1)
        if connector.connected:
            if connector.account.address:
                wallet_address = connector.account.address
                wallet_address: str = Address(wallet_address).to_str(is_bounceable=False)

                # Update user wallet in database.
                users_table.update_wallet(callback.from_user.id, wallet_address)

                await callback.message.edit_text(
                    text=translate(callback, strings, "success"),
                    reply_markup=MainModule.modules["wallet"].keyboard_finish(callback)
                )

                # Stop timer.
                break
    else:
        await callback.message.edit_text(
            text=translate(callback, strings, "failed"),
            reply_markup=MainModule.modules["wallet"].keyboard_finish(callback)
        )
    return None