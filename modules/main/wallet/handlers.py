import asyncio

from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from pytonconnect import TonConnect
from pytoniq_core import Address

from modules.main import MainModule
from markdown import Markdown
from core.config import users_table
from utils import translate, wallet_connector


@MainModule.router.callback_query(F.data == "wallet")
async def wallet(connector) -> None:
    for i in range(1, 180):
        await asyncio.sleep(1)
        if connector.connected:
            if connector.account.address:
                wallet_address = connector.account.address
                wallet_address = Address(wallet_address).to_str(is_bounceable=False)
                print(f'Connected with address: {wallet_address}')
                break
            return