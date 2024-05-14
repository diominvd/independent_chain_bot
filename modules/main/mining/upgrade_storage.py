import asyncio
import datetime

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from core.config import mining_table, users_table
from markdown import Markdown
from modules import MainModuleStates
from modules.main import MainModule
from translator import Translator


@MainModule.router.callback_query(StateFilter(MainModuleStates.upgrades), F.data == "upgrade_storage")
@users_table.update_last_activity
async def upgrade_storage(callback: CallbackQuery, state: FSMContext) -> None:
    user_data: dict = users_table.get_user(callback.from_user.id)
    user_mining_data: list = mining_table.get_user(callback.from_user.id)

    storage: int = user_mining_data[1]

    strings: dict[str, dict] = {
        "alert": {
            "ru": f"Уровень хранилища повышен до {storage + 1} ⬆️",
            "en": f"Storage level increased to {storage + 1} ⬆️"
        },
        "error": {
            "ru": "Недостаточно $tINCH для улучшения.",
            "en": "Not enough $tINCH to improve."
        }
    }

    price: float = round(float(75 * 2.2**(storage-1) * (1-mining_table.upgrade_discount)))

    if price > user_data["balance"]:
        await callback.answer(
            text=Translator.text(callback, strings, "error"),
            show_alert=True)
    else:
        users_table.update_balance(callback.from_user.id, "-", price)
        mining_table.update_storage(callback.from_user.id)

        await state.set_state(MainModuleStates.upgrades)

        await callback.answer(
            text=Translator.text(callback, strings, "alert"),
            show_alert=True)

        await MainModule.modules["mining"].upgrades_(callback, state)
    return None