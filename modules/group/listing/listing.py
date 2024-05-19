from aiogram.filters import Command
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from pytonapi import Tonapi

from core.config import users_table
from core.secrets import TON_API
from markdown import Markdown
from modules.group import GroupModule
from translator import Translator


async def get_project_balance() -> float:
    wallet_address: str = "UQA0IvXBnVMRI9BqM8GK-KeMPam7QBhAyiPAdfJUQ-Zzx_rk"
    ton: Tonapi = Tonapi(api_key=TON_API)
    balance: float = ton.accounts.get_info(wallet_address).balance.to_amount()
    return balance


@GroupModule.router.message(Command("listing"))
@users_table.update_last_activity
async def listing_(message: Message, state: FSMContext) -> None:
    balance: float = await get_project_balance()

    strings: dict[str, dict] = {
        "support": {
            "ru": (f"Согласно {Markdown.url('официальной документации', 'https://docs.google.com/forms/d/e/1FAIpQLSf4g-MB6BBYi8SVcloxAEc4tXQ-4034ngTEGjIsyaqGscjl8w/viewform?pli=1')} "
                   f"децентрализованной биржи DeDust.io для размещения на бирже требуется первоначальный капитал в "
                   f"размере 2000 {Markdown.bold('TON')} или {Markdown.bold('USDT')} в соответствующем эквиваленте.\n\n"
                   f"{Markdown.bold('Собрано')}: {balance} TON\n"
                   f"{Markdown.bold('Осталось собрать')}: {2000 - balance} TON"),
            "en": (f"According to the {Markdown.url('official documentation', 'https://docs.google.com/forms/d/e/1FAIpQLSf4g-MB6BBYi8SVcloxAEc4tXQ-4034ngTEGjIsyaqGscjl8w/viewform?pli=1')} "
                   f"of the decentralized exchange DeDust.io initial capital in the amount of "
                   f"2000 {Markdown.bold('TON')} or {Markdown.bold('USDT')} in the corresponding equivalent is required for listing.\n\n"
                   f"{Markdown.bold('Collected')}: {balance} TON\n"
                   f"{Markdown.bold('It remains to collect')}: {2000 - balance} TON")
        }
    }

    await message.answer(
        text=Translator.text(message, strings, "support"),
        reply_markup=GroupModule.modules["listing"].keyboard(message)
    )
    return None
