from aiogram import F, types
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from pytonapi import Tonapi

from core.config import users_table, bot
from core.secrets import TON_API
from markdown import Markdown
from modules.group import GroupModule
from translator import Translator


@GroupModule.router.message(Command("leaderboard"))
@users_table.update_last_activity
async def leaderboard_(message: Message, state: FSMContext) -> None:
    query: str = f"SELECT username, balance FROM users ORDER BY balance DESC LIMIT 10"
    leaders: list = users_table.select(query, ())

    text: str = f"{Markdown.bold('Таблица лидеров')}:\n"
    for i in range(len(leaders)):
        index = i + 1
        text += f"{index}. @{leaders[i][0]} - {leaders[i][1]} $tINCH\n"

    query: str = f"SELECT username, balance, (SELECT COUNT(DISTINCT balance) + 1 FROM users WHERE balance > t1.balance) AS position FROM users AS t1 WHERE user_id = {message.from_user.id}"
    user: tuple = users_table.select(query, ())[0]

    text += f"\n{user[2]}. @{user[0]} - {user[1]} $tINCH"

    if message.chat.type == "private":
        await message.answer(text=text)
    elif F.chat.type == "supergroup":
        await message.reply(text=text)
    return None

