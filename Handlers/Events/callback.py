import asyncio

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

import Text as txt
import utils as u
from Handlers.Events import strings
from Keyboards.Inline.events import keyboard
from States import DefaultStates
from config import dispatcher, bot, database as db


@dispatcher.callback_query(F.data == "events")
@u.update_last_activity
async def events(event: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(DefaultStates.events)
    user_language: str = db.get_user_language(user_id=event.from_user.id)
    await event.message.edit_text(
        text=txt.translate_text(strings, "events", user_language),
        reply_markup=keyboard(user_language))
    return None


async def send_top() -> None:
    while True:
        await asyncio.sleep(21600)
        db.cursor.execute("""SELECT referals FROM users ORDER BY referals DESC LIMIT 5""")
        top = [i[0] for i in db.cursor.fetchall()]
        users: list = [i[0] for i in db.get_all_users_id()]
        for user in users:
            user_language: str = db.get_user_language(user_id=user)
            await bot.send_message(
                chat_id=user,
                text=txt.translate_text(strings, "top", user_language, top))