from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from administration.handlers import admin_router
from administration.keyboards.mail_kb import mail_kb
from administration.middlewares.send_admin_panel import send_admin_panel
from administration.states import AdminStates
from config import database, bot
from utils.translator import translate


@admin_router.message(StateFilter(AdminStates.mail_username))
async def ru_mail(message: Message, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "request_text": {
            "ru": "Отправьте текст сообщения. После этого сообщение будет отправлено пользователю.",
            "en": "Send the text of the message. After that, the message will be sent to the user."
        }
    }

    await state.update_data(username=message.text.split("@")[1])
    await state.set_state(AdminStates.mail_message)

    await bot.edit_message_reply_markup(
        chat_id=message.from_user.id,
        message_id=message.message_id - 1,
        reply_markup=None
    )

    await bot.send_message(
        text=translate(message, strings["request_text"]),
        chat_id=message.from_user.id,
        reply_markup=mail_kb(message)
    )
    return None


@admin_router.message(StateFilter(AdminStates.mail_message))
async def en_mail(message: Message, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "mail_result": {
            "ru": f"Сообщение успешно отправлено.",
            "en": f"The message has been sent successfully."
        }
    }

    await state.update_data(en=message.text)

    await bot.edit_message_reply_markup(
        chat_id=message.from_user.id,
        message_id=message.message_id - 1,
        reply_markup=None
    )

    state_data: dict = await state.get_data()
    username: str = state_data["username"]

    await bot.send_message(
        chat_id=database.get_user_id(username),
        text=message.text
    )

    await bot.send_message(
        chat_id=message.from_user.id,
        text=translate(message, strings["mail_result"]),
    )

    await state.set_state(AdminStates.admin_panel)
    await send_admin_panel(message, state)
    return None