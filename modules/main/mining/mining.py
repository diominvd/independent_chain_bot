import datetime

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from core.config import mining_table, users_table
from markdown import Markdown
from modules import MainModuleStates
from modules.main import MainModule
from translator import Translator


@MainModule.router.callback_query(F.data == "mining")
@users_table.update_last_activity
async def mining_(callback: CallbackQuery, state: FSMContext) -> None:
    # Check the wallet binding.
    if await MainModule.modules["mining"].check_wallet_bind(callback) is False:
        strings: dict[str, dict] = {
            "check": {
                "ru": "Привяжите кошелёк Ton Space для доступа к функции добыче.",
                "en": "Link a Ton Space wallet to access the mining function."
            }
        }
        await callback.answer(
            text=Translator.text(callback, strings, "check"),
            show_alert=True)
    else:
        # Stop alert.
        await callback.answer(show_alert=False)
        await state.set_state(MainModuleStates.mining)
        await state.update_data(data={"mining_message": callback.message.message_id})

        # Check user existence in mining table.
        if not mining_table.check_user(callback.from_user.id):
            mining_table.create_user(callback.from_user.id)

        user_mining_data: list = mining_table.get_user(callback.from_user.id)

        last_claim_time: datetime = mining_table.get_last_claim(callback.from_user.id)
        last_claim_formated = MainModule.modules['mining'].calculate_last_claim_time(callback, last_claim_time)

        strings: dict[str, dict] = {
            "mining": {
                "ru": (f"Добыча {Markdown.bold('$tINCH')} открыта 🔥\n\n"
                       f"{Markdown.url('Настоятельно рекомендуем ознакомиться с руководством по использованию данного раздела.', 
                                       "https://teletype.in/@inch_ton/inch_mining_ru")}\n\n"
                       f"Купленные усилители должны храниться на кошельке {Markdown.bold('Ton Space')}.\n\n"
                       f"{Markdown.bold('Последний сбор')}: {last_claim_formated}\n"
                       f"{Markdown.bold('Усилитель')}: x{round(user_mining_data[3]*mining_table.global_booster, 4)}\n"
                       f"{Markdown.bold('Количество сборов')}: {user_mining_data[4]}\n"
                       f"{Markdown.bold('Ваша добыча')}: {round(user_mining_data[5], 4)} $tINCH\n\n"),
                "en": (f"Mining {Markdown.bold('$tINCH')} is open 🔥\n\n"
                       f"{Markdown.url('We strongly recommend that you familiarize yourself with manual for using this section.', 
                                       "https://teletype.in/@inch_ton/inch_mining_en")}\n\n"
                       f"The purchased amplifiers must be stored on the {Markdown.bold('Ton Space')} wallet.\n\n"
                       f"{Markdown.bold('Last claim')}: {last_claim_formated}\n"
                       f"{Markdown.bold('Booster')}: x{round(user_mining_data[3]*mining_table.global_booster, 4)}\n"
                       f"{Markdown.bold('Number of claims')}: {user_mining_data[4]}\n"
                       f"{Markdown.bold('Your loot')}: {round(user_mining_data[5], 4)} $tINCH")
            }
        }
        try:
            await callback.message.edit_text(
                text=Translator.text(callback, strings, "mining"),
                reply_markup=MainModule.modules["mining"].keyboard(callback))
        except:
            pass
        return None