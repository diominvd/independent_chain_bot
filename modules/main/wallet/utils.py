import asyncio

from pytonconnect import TonConnect
from pytoniq_core import Address


async def generate_wallet_connect_url() -> tuple[TonConnect, str]:
    connector: TonConnect = TonConnect("https://raw.githubusercontent.com/diominvd/independent_chain_bot/main/modules/main/wallet/manifest.json")
    wallets_list: dict = TonConnect.get_wallets()
    connect_url: str = await connector.connect(wallets_list[0])
    return connector, connect_url


async def connect_wallet_timer(connector: TonConnect, time_limit: int) -> str| bool:
    for second in range(1, time_limit):
        await asyncio.sleep(1)
        if connector.connected:
            if connector.account.address:
                wallet_address = connector.account.address
                wallet_address: str = Address(wallet_address).to_str(is_bounceable=False)
                return wallet_address
    else:
        return False