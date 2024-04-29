from aiogram.types import Message, CallbackQuery

from config import bot, database
from keyboards.inline.subscribe_kb import subscribe_kb
from utils.translator import translate


async def check_subscribe(event: Message | CallbackQuery) -> bool:
    strings: dict[str, dict] = {
        "alert": {
            "ru": "Для использования бота подпишитесь на каналы проекта. После этого нажмите кнопку \"Проверить\".",
            "en": "To use the bot, subscribe to the project channels. After that, click \"Check\"."
        },
        "check_failed": {
            "ru": "Проверка не пройдена.",
            "en": "Verification failed."
        }
    }

    language: str = database.get_user_language(user_id=event.from_user.id)
    statuses: list = ["member", "administrator", "creator"]

    user_status = None
    if language == "ru":
        user_status = await bot.get_chat_member(chat_id="@inch_ru", user_id=event.from_user.id)
    elif language == "en":
        user_status = await bot.get_chat_member(chat_id="@inch_en", user_id=event.from_user.id)

    if user_status.status.split(".")[0] not in statuses:
        # Send message with channel link.
        if type(event).__name__ != "CallbackQuery":
            await bot.send_message(
                chat_id=event.from_user.id,
                text=translate(event, strings["alert"]),
                reply_markup=subscribe_kb(event)
            )
        elif type(event).__name__ == "CallbackQuery":
            await event.answer(text=translate(event, strings["check_failed"]))
        return False
    else:
        return True