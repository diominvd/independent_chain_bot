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
    connector = TonConnect(
        manifest_url='https://raw.githubusercontent.com/XaBbl4/pytonconnect/main/pytonconnect-manifest.json')
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
                return None


@MainModule.router.callback_query(F.data == "wallet")
async def h_wallet(callback: CallbackQuery, state: FSMContext) -> None:

    address: str = t_users.select(("wallet",), "user_id", callback.from_user.id)

    strings: dict[str, dict] = {
        "linked": {
            "ru": (f"К вашему профилю уже привязан кошелёк {md.bold('Ton Space')}:\n"
                   f"\n"
                   f"{md.monospaced(f'{address}')}\n"
                   f"\n"
                   f"Для привязки нового кошелька отправьте его адрес."),
            "en": (f"Your {md.bold('Ton Space')} wallet is already linked to your profile:\n"
                   f"\n"
                   f"{md.monospaced(f'{address}')}\n"
                   f"\n"
                   f"To link a new wallet, send its address.")
        },
        "not linked": {
            "ru": (f"Для привязки кошелька {md.bold('Ton Space')} отправьте его адрес.\n"
                   f"\n"
                   f"Обращаем внимание на то, что бот поддерживает только адреса {md.bold('Ton Space')} кошельков ⚠️"),
            "en": (f"To link a {md.bold('Ton Space')} wallet send its address.\n"
                   f"\n"
                   f"Please note that the bot only supports {md.bold('Ton Space')} wallets addresses ⚠️")
        }
    }

    await callback.answer(show_alert=False)

    connector, url = await generate_url()


    await callback.message.edit_text(
        text=Translator.text(callback, strings, "not linked"),
        reply_markup=MainModule.modules["wallet"].keyboard_connect(callback, url),
        disable_web_page_preview=True
    )

    await connect(connector, callback.from_user.id)


def unique(address: str) -> bool:
    if t_users.select(("wallet",), "wallet", address) is None:
        return True
    else:
        return False


@MainModule.router.message(StateFilter(WalletStates.address))
async def h_address(message: Message, state: FSMContext) -> None:

    address: str = message.text

    strings: dict[str, dict] = {
        "error": {
            "ru": (f"Некорректный адрес кошелька 🚫\n"
                   f"\n"
                   f"Адрес кошелька должен состоять из 48 символов.\n"
                   f"\n"
                   f"Проверьте соответствие адреса указанным требованиям и повторите попытку."),
            "en": (f"Incorrect wallet address 🚫\n"
                   f"\n"
                   f"The wallet address must consist of 48 characters.\n"
                   f"\n"
                   f"Check that the address meets the specified requirements and try again.")
        },
        "not unique": {
            "ru": (f"Данный адрес кошелька уже привязан к другому профилю 🚫\n"
                   f"\n"
                   f"Выберите другой адрес и повторите попытку."),
            "en": (f"This wallet address is already linked to another profile 🚫\n"
                   f"\n"
                   f"Select a different address and try again.")
        },
        "success": {
            "ru": f"Адрес кошелька успешно привязан к вашему профилю ✅",
            "en": f"The wallet address has been successfully linked to your profile ✅"
        }
    }

    state_data: dict = await state.get_data()

    if unique(address) is True:
        if len(address) != 48:
            try:
                await bot.edit_message_text(
                    chat_id=message.from_user.id,
                    message_id=state_data["anchor"],
                    text=Translator.text(message, strings, "error"),
                    reply_markup=MainModule.modules["wallet"].keyboard(message, "cancel")
                )
            except:
                pass
        else:
            await state.clear()

            t_users.assign("wallet", address, "user_id", message.from_user.id)

            await bot.edit_message_text(
                chat_id=message.from_user.id,
                message_id=state_data["anchor"],
                text=Translator.text(message, strings, "success"),
                reply_markup=MainModule.modules["wallet"].keyboard(message, "back")
            )
    else:
        await bot.edit_message_text(
            chat_id=message.from_user.id,
            message_id=state_data["anchor"],
            text=Translator.text(message, strings, "not unique"),
            reply_markup=MainModule.modules["wallet"].keyboard(message, "back")
        )

    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id
    )