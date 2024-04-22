from aiogram import F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from Keyboards.Inline import main_keyboard
import Parse as p
from config import bot, dispatcher, database
from States.Default import DefaultStates
import utils as u


@dispatcher.callback_query(F.data == "links")
async def links(callback: CallbackQuery, state: FSMContext):
    database.update_last_activity(int(callback.from_user.id))
    await bot.edit_message_text(
        text=u.translate_text(strings, "links", database.get_user_language(int(callback.from_user.id)), int(callback.from_user.id)),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id
    )
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=main_keyboard(database.get_user_language(int(callback.from_user.id)))
    )


def ru_links(*args) -> str:
    text: str = f"""Чтобы оставаться в курсе последних новостей - подпишитесь на наши социальные сети:\n{p.bold("Канал проекта")}: @inch_coin\n{p.bold("Канал разработки")}: @diominvdev\n{p.bold("Твиттер")}: x.com/inch_coin\n{p.bold("Whitepaper")}: clck.ru/3ACbkk\n{p.bold("Исходный код бота")}: clck.ru/3ACbju"""
    return text


def en_links(*args) -> str:
    text: str = f"""To stay up to date with the latest news, subscribe to our social networks:\n{p.bold("Project channel")}: @inch_coin\n{p.bold("Dev channel")}: @diominvdev\n{p.bold("Twitter")}: x.com/inch_coin\n{p.bold("Whitepaper")}: clck.ru/3ACbkk\n{p.bold("Bot source code")}: clck.ru/3ACbju"""
    return text


strings: dict = {
    "links": {
        "ru": ru_links,
        "en": en_links
    }
}