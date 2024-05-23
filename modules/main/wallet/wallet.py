from aiogram import F
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database import UsersTable
from modules.main import MainModule
from states import WalletStates
from utils import Markdown as md, Translator


@MainModule.router.callback_query(F.data == "wallet")
async def h_wallet(callback: CallbackQuery, state: FSMContext):

    address: str = UsersTable.select(("wallet", ), "user_id", callback.from_user.id)

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
    await state.set_state(WalletStates.address)
    await state.update_data(anchor=callback.message.message_id)

    if address == "NULL":
        await callback.message.edit_text(
            text=Translator.text(callback, strings, "not linked"),
            reply_markup=MainModule.modules["wallet"].keyboard(callback, "cancel"),
            disable_web_page_preview=True
        )
    else:
        await callback.message.edit_text(
            text=Translator.text(callback, strings, "linked"),
            reply_markup=MainModule.modules["wallet"].keyboard(callback, "cancel"),
            disable_web_page_preview=True
        )