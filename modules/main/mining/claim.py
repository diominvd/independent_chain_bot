import asyncio
import datetime

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from core.config import mining_table, users_table
from modules.main import MainModule
from translator import Translator


@MainModule.router.callback_query(F.data == "claim")
@users_table.check_wallet_black_list
@users_table.update_last_activity
async def claim(callback: CallbackQuery, state: FSMContext) -> None:
    # Update total boosters value from user wallet.
    MainModule.modules["mining"].update_boosters(callback.from_user.id)

    user_mining_data: list = mining_table.get_user(callback.from_user.id)
    current_time: datetime = datetime.datetime.now()
    last_claim_time: datetime = mining_table.get_last_claim(callback.from_user.id)
    time_difference: datetime = (current_time - last_claim_time).total_seconds()

    reactor: int = user_mining_data[0]
    storage: int = user_mining_data[1]
    booster: int = user_mining_data[3]

    # Calculate reward.
    if time_difference < storage * 3600 + 7200:
        if time_difference > storage * 3600:
            time_difference = storage * 3600

        reward: float = time_difference * reactor * 0.001 * booster * mining_table.global_booster
        mining_table.claim(callback.from_user.id, reward)

        await asyncio.sleep(0.5)

        strings: dict[str, dict] = {
            "claim_success": {
                "ru": f"Получено {round(reward, 4)} $tINCH",
                "en": f"Received {round(reward, 4)} $tINCH"
            }
        }

        await callback.answer(
            text=Translator.text(callback, strings, "claim_success"),
            show_alert=True)

        # Refresh data of callback message.
        await MainModule.modules["mining"].mining_(callback, state)
    else:
        strings: dict[str, dict] = {
            "claim_failed": {
                "ru": f"Ресурсы сгорели. Добыча перезапущена.",
                "en": f"Resources are burned. Mining restarted."
            }
        }

        await callback.answer(
            text=Translator.text(callback, strings, "claim_failed"),
            show_alert=True)
        mining_table.claim(callback.from_user.id, 0)

        # Refresh data of callback message.
        await MainModule.modules["mining"].mining_(callback, state)
    return None