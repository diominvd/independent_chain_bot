from aiogram import F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from Keyboards.Inline import main_keyboard, check_subscribe_keyboard
import Parse as p
from config import bot, dispatcher, database
from States.Default import DefaultStates
import utils as u


@dispatcher.callback_query(F.data == "coin")
async def coin(callback: CallbackQuery, state: FSMContext):
    database.update_last_activity(int(callback.from_user.id))
    await bot.edit_message_text(
        text=u.translate_text(strings, "coin", database.get_user_language(int(callback.from_user.id)), int(callback.from_user.id)),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id
    )
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=main_keyboard(database.get_user_language(int(callback.from_user.id)))
    )


def ru_coin(*args) -> str:
    text: str = f"""{p.bold("Монет отчеканено")}: 10 000 000 $INCH\n{p.bold("Контракт")}: {p.code("EQDRaPxN8MkJOJYX-adlBBFnhMlHfPzIgD7NtyM0dtiauCZL")}\n{p.bold("TONSCAN")}: clck.ru/3ACbvj"""
    return text


def en_coin(*args) -> str:
    text: str = f"""{p.bold("Coins minted")}: 10 000 000 $INCH\n{p.bold("Contract")}: {p.code("EQDRaPxN8MkJOJYX-adlBBFnhMlHfPzIgD7NtyM0dtiauCZL")}\n{p.bold("TONSCAN")}: clck.ru/3ACbvj"""
    return text


strings: dict = {
    "coin": {
        "ru": ru_coin,
        "en": en_coin
    }
}