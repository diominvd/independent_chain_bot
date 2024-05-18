import asyncio

from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.config import users_table, bot, codes_table
from modules import MainModuleStates
from modules.main import MainModule
from translator import Translator


@MainModule.router.message(StateFilter(MainModuleStates.codes))
@users_table.update_last_activity
async def code_handler(message: Message, state: FSMContext) -> None:
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id)

    response: list = codes_table.load_code(message.text)

    if len(response) != 0:
        code_data: list = response[0]
        if codes_table.update_code(code_data[1]):
            strings: dict[str, dict] = {
                "success": {
                    "ru": (f"Промокод успешно активирован ✅\n"
                           f"Вам начислено {code_data[3]} $tINCH."),
                    "en": (f"Promo code successfully activated ✅\n"
                           f"You are credited with {code_data[3]} $tINCH.")
                }
            }

            data: dict = await state.get_data()
            await state.clear()

            users_table.activate_code(message.from_user.id, code_data[3])

            await bot.edit_message_text(
                chat_id=message.from_user.id,
                message_id=data["codes_message"],
                text=Translator.text(message, strings, "success"),
                reply_markup=MainModule.modules["codes"].keyboard_close(message, "profile"))
    else:
        strings: dict[str, dict] = {
            "fail": {
                "ru": "Недействительный промокод 🚫\n",
                "en": "Invalid promo code 🚫\n",
            }
        }

        await message.answer(
            text=Translator.text(message, strings, "fail"))

        await asyncio.sleep(3)

        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.message_id+1)
    return None