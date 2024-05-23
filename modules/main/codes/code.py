import datetime

from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.config import bot
from database import t_users, t_users_codes, t_codes
from modules.main import MainModule
from states import CodesStates
from utils import Translator


@MainModule.router.message(StateFilter(CodesStates.code))
async def h_code(message: Message, state: FSMContext) -> None:

    signature: str = message.text
    code = t_codes.get(signature)

    state_data: dict = await state.get_data()

    if code is not None:
        strings: dict[str, dict] = {
            "success": {
                "ru": (f"Промокод успешно активирован ✅\n"
                       f"Начислено {code.value} $tINCH"),
                "en": (f"The promo code has been successfully activated ✅\n"
                       f"Accrued {code.value} $tINCH")
            }
        }

        await state.clear()

        t_users.increase("balance", code.value, "user_id", message.from_user.id)
        t_users_codes.assign("last_code", datetime.datetime.now(), "user_id", message.from_user.id)
        t_codes.activate(code)

        await bot.edit_message_text(
            chat_id=message.from_user.id,
            message_id=state_data["anchor"],
            text=Translator.text(message, strings, "success"),
            reply_markup=MainModule.modules["wallet"].keyboard(message, "back")
        )
    else:
        strings: dict[str, dict] = {
            "invalid": {
                "ru": f"Недействительный промокод 🚫",
                "en": f"Invalid promo code 🚫"
            }
        }
        try:
            await bot.edit_message_text(
                chat_id=message.from_user.id,
                message_id=state_data["anchor"],
                text=Translator.text(message, strings, "invalid"),
                reply_markup=MainModule.modules["wallet"].keyboard(message, "back")
            )
        except:
            pass

    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id
    )
