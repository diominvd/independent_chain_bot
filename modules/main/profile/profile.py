from aiogram import F
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.config import users_table
from markdown import Markdown
from modules.main import MainModule
from translator import Translator


@MainModule.router.message(F.chat.type == ChatType.PRIVATE, Command("profile"))
@MainModule.router.callback_query(F.data == "profile")
@users_table.check_wallet_black_list
@users_table.update_last_activity
async def profile_(event: Message | CallbackQuery, state: FSMContext) -> None:
    users_table.update_username(event.from_user.id, event.from_user.username)
    user_data: dict = users_table.get_user(event.from_user.id)
    strings: dict[str, dict] = {
        "profile": {
            "ru": (f"Привет, @{user_data['username']} 👋\n"
                   f"{Markdown.bold('Ваш UID')}: {user_data['project_id']}\n"
                   f"{Markdown.bold('Баланс')}: {round(user_data['balance'], 4)} $tINCH\n"
                   f"{Markdown.bold('Друзья')}: {user_data['referals']}\n"
                   f"{Markdown.bold('Ton Space')}: {Markdown.monospaced(user_data['wallet'])}\n\n"
                   f"{Markdown.bold('Реферальная ссылка')}:\n"
                   f"{Markdown.monospaced(f't.me/inch_coin_bot?start={event.from_user.id}')}\n"
                   f"(Нажмите, чтобы скопировать)"),
            "en": (f"Hello, @{user_data['username']} 👋\n"
                   f"{Markdown.bold('Your UID')}: {user_data['project_id']}\n"
                   f"{Markdown.bold('Balance')}: {round(user_data['balance'], 4)} $tINCH\n"
                   f"{Markdown.bold('Friends')}: {user_data['referals']}\n"
                   f"{Markdown.bold('Ton Space')}: {Markdown.monospaced(user_data['wallet'])}\n\n"
                   f"{Markdown.bold('Referal link')}:\n"
                   f"{Markdown.monospaced(f't.me/inch_coin_bot?start={event.from_user.id}')}\n"
                   f"(Click to copy)")
        }
    }

    await state.clear()

    match type(event).__name__:
        case "Message":
            await event.answer(
                text=Translator.text(event, strings, "profile"),
                reply_markup=MainModule.modules["profile"].keyboard(event))
        case "CallbackQuery":
            try:
                await event.message.edit_text(
                    text=Translator.text(event, strings, "profile"),
                    reply_markup=MainModule.modules["profile"].keyboard(event))
            except:
                pass
            finally:
                await event.answer(show_alert=False)
    return None
