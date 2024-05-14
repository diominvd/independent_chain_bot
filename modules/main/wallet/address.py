from aiogram import Dispatcher
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.config import users_table, bot
from modules import MainModuleStates
from modules.main import MainModule
from translator import Translator


async def check_wallet_uniqueness(user_id: int, address: str) -> bool:
    query: str = "SELECT wallet FROM users WHERE user_id != %s"
    values: tuple = tuple([user_id])
    wallets: list = [item[0] for item in users_table.select(query, values)]
    if wallet in wallets:
        return False
    else:
        return True


@MainModule.router.message(StateFilter(MainModuleStates.wallet))
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
            "ru": "Данный кошелёк уже привязан к другому профилю.",
            "en": "This wallet is already linked to another profile."
        }
    }

    data: dict = await state.get_data()

    wallet_address: str = message.text

    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id)

    if len(wallet_address) == 48:
        users_table.update_wallet(message.from_user.id, wallet_address)

        await bot.edit_message_text(
            chat_id=message.from_user.id,
            message_id=data["wallet_message"],
            text=Translator.text(message, strings, "success"),
            reply_markup=MainModule.modules["wallet"].keyboard_finish(message))
    else:
        if await check_wallet_uniqueness(message.from_user.id, wallet_address):
            await bot.edit_message_text(
                chat_id=message.from_user.id,
                message_id=data["wallet_message"],
                text=Translator.text(message, strings, "fail"),
                reply_markup=MainModule.modules["wallet"].keyboard_cancel(message))
        else:
            await bot.edit_message_text(
                chat_id=message.from_user.id,
                message_id=data["wallet_message"],
                text=Translator.text(message, strings, "not_unique"),
                reply_markup=MainModule.modules["wallet"].keyboard_cancel(message))
    return None