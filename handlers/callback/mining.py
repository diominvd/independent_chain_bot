import asyncio
import datetime

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import database, bot, mining_table
from handlers.callback import callback_router
from keyboards.inline.mining_kb import mining_kb
from markdown import markdown
from utils.translator import translate


@callback_router.callback_query(F.data == "mining")
@database.update_activity
async def mining_callback(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "description": {
            "ru": f"{markdown.bold('Вам доступна добыча $tINCH')}\n\n"
                  f"Для заполнения хранилища необходимо 4 часа реального времени.\n\n"
                  f"Если в течении 2-ух часов после заполнения хранилища не собрать $tINCH, то они безвозвратно сгорят 🔥\n\n"
                  f"Для сбора $tINCH нажмите соответствующую кнопку.",
            "en": f"{markdown.bold('$tINCH mining is available to you')}\n\n"
                  f"It takes 4 hours of real time to fully fill the storage.\n\n"
                  f"If you do not collect $tINCH within 2 hours after filling the vault, then they will irretrievably burn out 🔥\n\n"
                  f"To collect $tINCH, click the appropriate button."
        },
        "failed": {
            "ru": "Для доступа к добыче пригласите минимум трёх друзей.",
            "en": "Invite at least three friends to access the loot."
        }
    }

    if database.get_referals(callback) >= 3:
        await callback.answer(show_alert=False)
        await callback.message.edit_text(
            text=translate(callback, strings["description"]),
            reply_markup=mining_kb(callback)
        )
    else:
        await callback.answer(text=translate(callback, strings["failed"]), show_alert=True)
    return None


@callback_router.callback_query(F.data == "claim")
async def mining(callback: CallbackQuery):
    if not mining_table.check_miner_existence(callback):
        mining_table.create_user(callback)
    else:
        current_time = datetime.datetime.now()
        last_claim_time = mining_table.get_last_claim_time(callback)
        timer = (current_time - last_claim_time).total_seconds()

        if 0 < timer < 21600:
            if timer > 14400:
                timer = 14400
            profit = timer * 0.001
            mining_table.claim(callback, profit)

            strings: dict[str, dict] = {
                "claim_success": {
                    "ru": f"Получено {round(profit, 2)} $tINCH",
                    "en": f"Received {round(profit, 2)} $tINCH"
                }
            }

            await callback.answer(text=translate(callback, strings["claim_success"]))
            return None
        else:
            strings: dict[str, dict] = {
                "claim_failed": {
                    "ru": f"Ресурсы сгорели. Добыча перезапущена.",
                    "en": f"Resources are burned. Mining restarted."
                }
            }
            await callback.answer(text=translate(callback, strings["claim_failed"]))
