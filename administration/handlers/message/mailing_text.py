from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from administration.handlers import admin_router
from administration.keyboards.mail_kb import mail_kb
from administration.middlewares.send_admin_panel import send_admin_panel
from administration.middlewares.send_mailing import send_mailing
from administration.states import AdminStates
from config import bot
from utils.translator import translate


@admin_router.message(StateFilter(AdminStates.mailing_ru))
async def ru_mail(message: Message, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "request_en_message": {
            "ru": "Отправьте текст сообщения на английском языке. После этого рассылка будет автоматически отправлена.",
            "en": "Send the text of the message in English. After that, the newsletter will be sent automatically."
        }
    }

    await state.update_data(ru=message.text)
    await state.set_state(AdminStates.mailing_en)

    await bot.edit_message_reply_markup(
        chat_id=message.from_user.id,
        message_id=message.message_id - 1,
        reply_markup=None
    )

    await bot.send_message(
        text=translate(message, strings["request_en_message"]),
        chat_id=message.from_user.id,
        reply_markup=mail_kb(message)
    )
    return None


@admin_router.message(StateFilter(AdminStates.mailing_en))
async def en_mail(message: Message, state: FSMContext) -> None:
    await state.update_data(en=message.text)

    await bot.edit_message_reply_markup(
        chat_id=message.from_user.id,
        message_id=message.message_id - 1,
        reply_markup=None
    )

    state_data: dict = await state.get_data()
    result: list = await send_mailing(state_data)
    strings: dict[str, dict] = {
        "mailing_result": {
            "ru": f"Рассылка успешно отправлена.\n"
                  f"Всего пользователей: {result[0]}\n"
                  f"Успешно отправлено: {result[1]}\n"
                  f"Не отправлено: {result[2]}\n",
            "en": "The newsletter has been sent successfully.\n"
                  f"Total users: {result[0]}\n"
                  f"Successfully sent: {result[1]}\n"
                  f"Not sent: {result[2]}\n"
        }
    }
    response: str = translate(message, strings["mailing_result"])

    await bot.send_message(
        chat_id=message.from_user.id,
        text=response,
    )

    await state.set_state(AdminStates.admin_panel)
    await send_admin_panel(message, state)
    return None