import datetime

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from core.config import mining_table, users_table
from markdown import Markdown
from modules.main import MainModule
from translator import Translator


@MainModule.router.callback_query(F.data == "mining")
@users_table.update_last_activity
async def mining(callback: CallbackQuery, state: FSMContext) -> None:
    # Check the wallet binding.
    if await MainModule.modules["mining"].check_wallet_bind(callback) is False:
        return None

    # Stop alert.
    await callback.answer(show_alert=False)

    # Check user existence in mining table.
    if not mining_table.check_user(callback.from_user.id):
        mining_table.create_user(callback.from_user.id)

    user_data: list = mining_table.get_user(callback.from_user.id)
    strings: dict[str, dict] = {
        "mining": {
            "ru": (f"Добыча {Markdown.bold('$tINCH')} открыта 🔥\n\n"
                   f"Время заполнения хранилища - 4 часа. Чтобы собрать добычу нажмите соответствующую кнопку. "
                   f"После заполнения хранилища у вас будет 2 часа, чтобы собрать $tINCH. "
                   f"В противном случае добыча будет утеряна.\n\n"
                   f"{Markdown.bold('Виды усилителей')}:\n"
                   f"🥉 Бронзовый - x1.1\n"
                   f"🥈 Серебрянный - x1.2\n"
                   f"🥇 Золотой - x1.3\n\n"
                   f"При наличии нескольких усилителей значения множителей перемножаются.\n\n"
                   f"{Markdown.bold('Усилитель')}: x{round(user_data[0], 4)}\n"
                   f"{Markdown.bold('Количество сборов')}: {user_data[1]}\n"
                   f"{Markdown.bold('Ваша добыча')}: {round(user_data[2], 4)} $tINCH"),
            "en": (f"Mining {Markdown.bold('$tINCH')} is open 🔥\n\n"
                   f"The storage time is 4 hours. To collect the loot, click the appropriate button. "
                   f" After filling the vault, you will have 2 hours to collect $tINCH. "
                   f" Otherwise, the loot will be lost.\n\n"
                   f"{Markdown.bold('Types of amplifiers')}:\n"
                   f"🥉 Bronze - x1.1\n"
                   f"🥈 Silver - 1.2\n"
                   f"🥇 Gold - x1.3\n\n"
                   f"If there are several amplifiers, the multiplier values are multiplied.\n\n"
                   f"{Markdown.bold('Booster')}: x{round(user_data[0], 4)}\n"
                   f"{Markdown.bold('Number of fees')}: {user_data[1]}\n"
                   f"{Markdown.bold('Your loot')}: {round(user_data[2], 4)} $tINCH")
        }
    }

    await callback.message.edit_text(
        text=Translator.text(callback, strings, "mining"),
        reply_markup=MainModule.modules["mining"].keyboard(callback))
    return None


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
        reward: float = time_difference * 0.001 * booster
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
        await mining(callback)
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
