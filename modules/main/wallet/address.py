from aiogram import Dispatcher
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.config import users_table, bot
from core.secrets import WALLETS_BLACK_LIST
from modules import MainModuleStates
from modules.main import MainModule
from translator import Translator


@MainModule.router.message(StateFilter(MainModuleStates.wallet))
@users_table.check_wallet_black_list
@users_table.update_last_activity
async def wallet(message: Message, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "success": {
            "ru": "Кошелёк успешно подключён ✅",
            "en": "The wallet has been successfully connected ✅"
        },
        "fail": {
            "ru": ("Некорректный адрес кошелька 🚫\n"
                   "Длина адреса должна быть равна 48 знакам. Проверьте правильность написания адреса и повторите попытку."),
            "en": ("Invalid wallet address 🚫\n"
                   "The length of the address must be 48 characters. Check that the address is spelled correctly and try again.")
        },
        "not_unique": {
            "ru": "Данный кошелёк уже привязан к другому профилю 🚫\nПопробуйте другой адрес кошелька.",
            "en": "This wallet is already linked to another profile 🚫\nTry a different wallet address."
        },
        "ban": {
            "ru": "Данный адрес кошелька находится в чёрном списке🚫\nПопробуйте привязать другой адрес.",
            "en": "This wallet address is in the blacklist.🚫\nTry to link another address."
        }
    }

    data: dict = await state.get_data()

    wallet_address: str = message.text

    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id)

    if users_table.check_wallet_unique(wallet_address):
        if wallet_address not in WALLETS_BLACK_LIST:
            if len(wallet_address) == 48:
                users_table.update_wallet(message.from_user.id, wallet_address)

                await bot.edit_message_text(
                    chat_id=message.from_user.id,
                    message_id=data["wallet_message"],
                    text=Translator.text(message, strings, "success"),
                    reply_markup=MainModule.modules["wallet"].keyboard_finish(message))
            else:
                await bot.edit_message_text(
                    chat_id=message.from_user.id,
                    message_id=data["wallet_message"],
                    text=Translator.text(message, strings, "fail"),
                    reply_markup=MainModule.modules["wallet"].keyboard_cancel(message))
        else:
            await bot.edit_message_text(
                chat_id=message.from_user.id,
                message_id=data["wallet_message"],
                text=Translator.text(message, strings, "ban"),
                reply_markup=MainModule.modules["wallet"].keyboard_cancel(message))
    else:
        await bot.edit_message_text(
            chat_id=message.from_user.id,
            message_id=data["wallet_message"],
            text=Translator.text(message, strings, "not_unique"),
            reply_markup=MainModule.modules["wallet"].keyboard_cancel(message))
    return None