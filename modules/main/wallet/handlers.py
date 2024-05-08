from aiogram import F
from aiogram.types import CallbackQuery

from modules.main import MainModule
from core.config import users_table
from translator import Translator


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

    # Stop alert:
    await callback.answer(show_alert=False)

    # Generate link for Ton Space connect.
    connector, connect_url = MainModule.modules["wallet"].generate_wallet_connect_url()

    await callback.message.edit_text(
        text=Translator.text(callback, strings, "information"),
        reply_markup=MainModule.modules["wallet"].keyboard_connect(callback, connect_url))

    # Start connect timer.
    connect_result: str | bool = MainModule.modules["wallet"].connect_wallet_timer(connector, 600)
    if connect_result:
        wallet_address: str = connect_result
        users_table.update_wallet(callback.from_user.id, wallet_address)

        await callback.message.edit_text(
            text=Translator.text(callback, strings, "success"),
            reply_markup=MainModule.modules["wallet"].keyboard_finish(callback))
    else:
        await callback.message.edit_text(
            text=Translator.text(callback, strings, "failed"),
            reply_markup=MainModule.modules["wallet"].keyboard_finish(callback))
    return None