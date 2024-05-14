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


async def format_hour(hour: int) -> str:
    if hour == 1:
        return f"{hour} час"
    elif 2 <= hour <= 5:
        return f"{hour} часа"
    elif 6 <= hour:
        return f"{hour} часов"


@MainModule.router.callback_query(F.data == "upgrades")
@users_table.update_last_activity
async def upgrades_(callback: CallbackQuery, state: FSMContext) -> None:
    user_mining_data: list = mining_table.get_user(callback.from_user.id)
    user_data: dict = users_table.get_user(callback.from_user.id)

    reactor: int = user_mining_data[0]
    storage: int = user_mining_data[1]

    reactor_price: float = float(150 * 2.2**(reactor-1)) * (1-mining_table.upgrade_discount)
    storage_price: float = float(75 * 2.2**(storage-1) * (1-mining_table.upgrade_discount))

    strings: dict[str, dict] = {
        "upgrades": {
            "ru": (f"Покупка улучшений позволит увеличить количество добываемых $tINCH ⬆️\n\n"
                   f"⚙️ {Markdown.bold('Реактор')}: {user_mining_data[0]} уровень\n"
                   f"🕑 {Markdown.bold('Хранилище')}: {user_mining_data[1]} уровень\n"
                   f"🤖 {Markdown.bold('Автосбор')}: {'Выключен' if user_mining_data[2] == 0 else 'Включён'}\n\n"
                   f"• {Markdown.bold(f'Реактор')} - влияет на скорость добычи. Чем выше уровень, тем большее $tINCH.\n"
                   f"• {Markdown.bold(f'Хранилище')} - влияет на время добычи. Чем выше уровень, тем большее время можно добывать $tINCH.\n"
                   f"• {Markdown.bold(f'Автосбор')} - подключает бота, который на протяжении 12 часов будет автономно собирать $tINCH. "
                   f"Автоматически включается у владельцев INCH COIN BOOSTERS.\n\n"
                   f"{Markdown.bold('Баланс')}: {user_data['balance']} $tINCH\n\n"
                   f"{Markdown.bold('Стоимость улучшений')}:\n"
                   f"Реактор ({round((reactor + 1) * 0.001, 3)}/сек): {round(reactor_price)} $tINCH\n"
                   f"Хранилище ({await format_hour(storage + 1)}): {round(storage_price)} $tINCH"),
            "en": (f"Buying upgrades will increase the amount of $tINCH mined ⬆️\n\n"
                   f"⚙️ {Markdown.bold('Reactor')}: {user_mining_data[0]} уровень\n"
                   f"🕑 {Markdown.bold('Storage')}: {user_mining_data[1]} уровень\n"
                   f"🤖 {Markdown.bold('Auto claim')}: {'Turned off' if user_mining_data[2] == 0 else 'Turned on'}\n\n"
                   f"• {Markdown.bold(f'Reactor')} - affects the production rate. The higher the level, the greater the $tINCH.\n"
                   f"• {Markdown.bold(f'Storage')} - affects the mining time. The higher the level, the longer it takes to mine $tINCH.\n"
                   f"• {Markdown.bold(f'Auto claim')} - connects a bot that will collect $tINCH offline for 12 hours. "
                   f"It is automatically enabled for owners of INCH COIN BOOSTERS.\n\n"
                   f"{Markdown.bold('Balance')}: {user_data['balance']} $tINCH\n\n"
                   f"{Markdown.bold('Cost of improvements')}:\n"
                   f"Reactor ({round((reactor + 1) * 0.001, 3)}/sec): {round(reactor_price)} $tINCH\n"
                   f"Storage ({storage + 1} hours): {round(storage_price)} $tINCH"),
        }
    }

    await callback.answer(show_alert=False)
    await state.set_state(MainModuleStates.upgrades)

    await callback.message.edit_text(
        text=Translator.text(callback, strings, "upgrades"),
        reply_markup=MainModule.modules["mining"].keyboard_upgrades(callback))
    return None


def calculate(a: int, b: int, c: int) -> None:
    """

    :param a:
    :param b:
    :param c:
    :return:
    """
    return None