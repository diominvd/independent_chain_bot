from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from core.config import bot
from database import t_users
from modules.main import MainModule
from states import WalletStates
from utils import Markdown as md, Translator


import asyncio
from tonsdk.utils import Address

from pytonconnect import TonConnect
from pytonconnect.storage import FileStorage
from pytonconnect.exceptions import TonConnectError


async def generate_url():
    connector = TonConnect(manifest_url='https://raw.githubusercontent.com/diominvd/independent_chain_bot/main/modules/main/wallet/manifest.json')

    wallets: list = connector.get_wallets()
    connect_url = await connector.connect(wallets[0])

    return connector, connect_url


async def connect(connector, user_id: int):
    connected = await connector.wait_for_connection()

    for i in range(300):
        await asyncio.sleep(1)
        if connected:
            if connector.connected and connector.account.address:
                wallet: str = Address(connector.account.address).to_string(is_user_friendly=True,  is_url_safe=True, is_bounceable=False)
                t_users.assign("wallet", wallet, "user_id", user_id)
                await connector.disconnect()
                return True


@MainModule.router.callback_query(F.data == "wallet")
async def h_wallet(callback: CallbackQuery, state: FSMContext) -> None:

    address: str = t_users.select(("wallet",), "user_id", callback.from_user.id)

    strings: dict[str, dict] = {
        "linked": {
            "ru": (f"К вашему профилю уже привязан кошелёк {md.bold('Ton Space')}:\n"
                   f"\n"
                   f"{md.monospaced(f'{address}')}"),
            "en": (f"Your {md.bold('Ton Space')} wallet is already linked to your profile:\n"
                   f"\n"
                   f"{md.monospaced(f'{address}')}\n")
        },
        "not linked": {
            "ru": (f"Для привязки кошелька {md.bold('Ton Space')} воспользуйтесь соответствующей кнопкой.\n"
                   f"\n"
                   f"Обращаем внимание на то, что бот поддерживает только адреса {md.bold('Ton Space')} кошельков ⚠️"),
            "en": (f"To link a {md.bold('Ton Space')} wallet use the appropriate button.\n"
                   f"\n"
                   f"Please note that the bot only supports {md.bold('Ton Space')} wallets addresses ⚠️")
        },
        "success": {
            "ru": f"Адрес кошелька успешно привязан к вашему профилю ✅",
            "en": f"The wallet address has been successfully linked to your profile ✅"
        }
    }

    await callback.answer(show_alert=False)

    connector, url = await generate_url()

    if address == "NULL":
        await callback.message.edit_text(
            text=Translator.text(callback, strings, "not linked"),
            reply_markup=MainModule.modules["wallet"].keyboard_connect(callback, url),
            disable_web_page_preview=True
        )

        await connect(connector, callback.from_user.id)

        await callback.message.edit_text(
            text=Translator.text(callback, strings, "success"),
            reply_markup=MainModule.modules["wallet"].keyboard(callback),
            disable_web_page_preview=True
        )
    else:
        await callback.message.edit_text(
            text=Translator.text(callback, strings, "linked"),
            reply_markup=MainModule.modules["wallet"].keyboard(callback),
            disable_web_page_preview=True
        )