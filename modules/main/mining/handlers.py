from aiogram import F
from aiogram.types import CallbackQuery
import datetime

from modules.main import MainModule
from core.config import mining_table
from markdown import Markdown
from utils import translate


@MainModule.router.callback_query(F.data == "mining")
async def mining(callback: CallbackQuery) -> None:
    # Stop alert:
    await callback.answer(show_alert=False)

    if not mining_table.check_user(callback.from_user.id):
        mining_table.create_user(callback.from_user.id)
    user_data: list = mining_table.get_user(callback.from_user.id)

    strings: dict[str, dict] = {
        "mining": {
            "ru": f"Добыча {Markdown.bold('$tINCH')} открыта 🔥\n\n"
                  f"Время заполнения хранилища - 4 часа. Чтобы собрать добычу нажмите соответствующую кнопку. "
                  f"После заполнения хранилища у вас будет 2 часа, чтобы собрать $tINCH. "
                  f"В противном случае добыча будет утеряна.\n\n"
                  f"Количество сборов: {user_data[0]}\n"
                  f"Ваша добыча: {user_data[1]} $tINCH",
            "en": f"Mining {Markdown.bold('$tINCH')} is open 🔥\n\n"
                  f"The storage time is 4 hours. To collect the loot, click the appropriate button. "
                  f" After filling the vault, you will have 2 hours to collect $tINCH. "
                  f" Otherwise, the loot will be lost.\n\n"
                  f"Number of fees: {user_data[0]}\n"
                  f"Your loot: {user_data[1]} $tINCH"
        }
    }

    await callback.message.edit_text(
        text=translate(callback, strings, "mining"),
        reply_markup=MainModule.modules["mining"].keyboard(callback)
    )


@MainModule.router.callback_query(F.data == "claim")
async def claim(callback: CallbackQuery) -> None:
    current_time: datetime = datetime.datetime.now()
    last_claim_time: datetime = mining_table.get_last_claim(callback.from_user.id)
    time_difference: datetime = (current_time - last_claim_time).total_seconds()

    if 0 < time_difference < 21600:
        if time_difference > 14400:
            time_difference = 14400

        reward: float = time_difference * 0.001
        mining_table.claim(callback.from_user.id, reward)

        strings: dict[str, dict] = {
            "claim_success": {
                "ru": f"Получено {round(reward, 2)} $tINCH",
                "en": f"Received {round(reward, 2)} $tINCH"
            }
        }

        await callback.answer(
            text=translate(callback, strings, "claim_success"),
            show_alert=True
        )

        await mining(callback)
    else:
        strings: dict[str, dict] = {
            "claim_failed": {
                "ru": f"Ресурсы сгорели. Добыча перезапущена.",
                "en": f"Resources are burned. Mining restarted."
            }
        }

        await callback.answer(
            text=translate(callback, strings, "claim_failed"),
            show_alert=True
        )
        mining_table.claim(callback.from_user.id, 0)
    return None
