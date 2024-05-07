from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from pytonconnect import TonConnect

from modules.main import MainModule
from markdown import Markdown
from core.config import users_table
from utils import translate, wallet_connector


@MainModule.router.message(Command("profile"))
@MainModule.router.callback_query(F.data == "profile")
async def profile(event: Message | CallbackQuery) -> None:
    user_data: dict = users_table.get_user(event.from_user.id)
    strings: dict[str, dict] = {
        "profile": {
            "ru": f"Привет, @{user_data['username']} 👋\n"
                  f"{Markdown.bold('Ваш UID')}: {user_data['project_id']}\n"
                  f"{Markdown.bold('Баланс')}: {user_data['balance']} $tINCH\n"
                  f"{Markdown.bold('Друзья')}: {user_data['referals']}\n"
                  f"{Markdown.bold('Ton Space')}: {user_data['wallet']}\n\n"
                  f"{Markdown.bold('Реферальная ссылка:')}:\n"
                  f"{Markdown.monospaced(f't.me/inch_coin_bot?start={event.from_user.id}')}\n"
                  f"(Нажмите, чтобы скопировать)",
            "en": f"Hello, @{user_data['username']} 👋\n"
                  f"{Markdown.bold('Your UID')}: {user_data['project_id']}\n"
                  f"{Markdown.bold('Balance')}: {user_data['balance']} $tINCH\n"
                  f"{Markdown.bold('Friends')}: {user_data['referals']}\n"
                  f"{Markdown.bold('Ton Space')}: {user_data['wallet']}\n\n"
                  f"{Markdown.bold('Referal link:')}:\n"
                  f"{Markdown.monospaced(f't.me/inch_coin_bot?start={event.from_user.id}')}\n"
                  f"(Click to copy)"
        }
    }

    connector: TonConnect = TonConnect(manifest_url="https://raw.githubusercontent.com/XaBbl4/pytonconnect/main/pytonconnect-manifest.json")
    wallets_list: dict = TonConnect.get_wallets()
    wallet_connect: str = await connector.connect(wallets_list[0])

    match type(event).__name__:
        case "Message":
            await event.answer(
                text=translate(event, strings, "profile"),
                reply_markup=MainModule.modules["profile"].keyboard(event, wallet_connect)
            )
        case "CallbackQuery":
            try:
                await event.message.edit_text(
                    text=translate(event, strings, "profile"),
                    reply_markup=MainModule.modules["profile"].keyboard(event, wallet_connect)
                )
            except:
                pass
            finally:
                await event.answer(show_alert=False)
    return None