from aiogram import F
from aiogram.enums import ChatType
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.config import bot
from database import UsersTable
from modules.main import MainModule
from states import WalletStates
from utils import Markdown as md, Translator


def unique(address: str) -> bool:
    if UsersTable.f_wallet("wallet", address) is None:
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

    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id
    )

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

            UsersTable.assign("wallet", address, "user_id", message.from_user.id)

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
