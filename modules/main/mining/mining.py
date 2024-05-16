import datetime

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from core.config import mining_table, users_table
from markdown import Markdown
from modules import MainModuleStates
from modules.main import MainModule
from translator import Translator

from database import MiningTableUsers


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

    # Stop alert.
    await callback.answer(show_alert=False)
    await state.set_state(MainModuleStates.mining)
    await state.update_data(data={"mining_message": callback.message.message_id})

    # Check user existence in mining table.
    if not mining_table.check_user(callback.from_user.id):
        mining_table.create_user(callback.from_user.id)

    user_mining_data: MiningTableUsers = mining_table.get_user(callback.from_user.id)

    last_claim_time: datetime = mining_table.get_last_claim(callback.from_user.id)
    last_claim_formated = MainModule.modules['mining'].calculate_last_claim_time(callback, last_claim_time)

    strings: dict[str, dict] = {
        "mining": {
            "ru": (f"Добыча {Markdown.bold('$tINCH')} открыта 🔥\n\n"
                   f"Время заполнения хранилища определяется его уровнем. Чтобы собрать добычу нажмите соответствующую кнопку. "
                   f"После заполнения хранилища у вас будет 2 часа, чтобы собрать $tINCH. "
                   f"В противном случае добыча будет утеряна.\n\n"
                   f"Для ознакомления с механикой \"Улучшений\" ознакомьтесь с соответствующим разделом.\n\n"
                   f"{Markdown.bold('Виды усилителей')}:\n"
                   f"🥉 Бронзовый - x1.1\n"
                   f"🥈 Серебрянный - x1.2\n"
                   f"🥇 Золотой - x1.3\n"
                   f"💎 Особенные\n\n"
                   f"Купленные усилители должны храниться на кошельке {Markdown.monospaced('Ton Space')}. "
                   f"При наличии нескольких усилителей значения множителей перемножаются.\n\n"
                   f"{Markdown.bold('Последний сбор')}: {last_claim_formated}\n"
                   f"{Markdown.bold('Усилитель')}: x{round(user_mining_data["ищ"]*mining_table.global_booster, 4)}\n"
                   f"{Markdown.bold('Количество сборов')}: {user_mining_data["claims"]}\n"
                   f"{Markdown.bold('Ваша добыча')}: {round(user_mining_data["amount"], 4)} $tINCH\n\n"),
            "en": (f"Mining {Markdown.bold('$tINCH')} is open 🔥\n\n"
                   f"The storage fill time is determined by its level. To collect the loot, click the appropriate button. "
                   f" After filling the vault, you will have 2 hours to collect $tINCH. "
                   f" Otherwise, the loot will be lost.\n\n"
                   f"To familiarize yourself with the mechanics of \"Improvements\", read the relevant section.\n\n"
                   f"{Markdown.bold('Types of amplifiers')}:\n"
                   f"🥉 Bronze - x1.1\n"
                   f"🥈 Silver - 1.2\n"
                   f"🥇 Gold - x1.3\n"
                   f"💎 Special\n\n"
                   f"The purchased amplifiers must be stored on the {Markdown.monospaced('Ton Space')} wallet. "
                   f"If there are several amplifiers, the multiplier values are multiplied.\n\n"
                   f"{Markdown.bold('Last claim')}: {last_claim_formated}\n"
                   f"{Markdown.bold('Booster')}: x{round(user_mining_data["booster"]*mining_table.global_booster, 4)}\n"
                   f"{Markdown.bold('Number of fees')}: {user_mining_data["claims"]}\n"
                   f"{Markdown.bold('Your loot')}: {round(user_mining_data["amount"], 4)} $tINCH")
        }
    }
    try:
        await callback.message.edit_text(
            text=Translator.text(callback, strings, "mining"),
            reply_markup=MainModule.modules["mining"].keyboard(callback))
    except:
        pass
    return None