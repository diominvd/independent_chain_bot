import datetime

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from core.config import mining_table, users_table
from modules.main import MainModule
from translator import Translator


@MainModule.router.callback_query(F.data == "claim")
@users_table.update_last_activity
async def claim(callback: CallbackQuery, state: FSMContext) -> None:
    # Update total boosters value from user wallet.
    MainModule.modules["mining"].update_boosters(callback.from_user.id)

    user_data: list = mining_table.get_user(callback.from_user.id)
    current_time: datetime = datetime.datetime.now()
    last_claim_time: datetime = mining_table.get_last_claim(callback.from_user.id)
    time_difference: datetime = (current_time - last_claim_time).total_seconds()

    # Calculate reward.
    if 0 < time_difference < 21600:
        if time_difference > 14400:
            time_difference = 14400

        booster: float = user_data[0]
        reward: float = time_difference * 0.002 * booster
        mining_table.claim(callback.from_user.id, reward)

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
        await MainModule.modules["mining"].mining(callback)
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
    return None