from aiogram.filters import Command
from aiogram.types import Message

from config import bot, dispatcher, database as db
from Keyboards.Inline import mailing_keyboard
from secret import bot_admins


@dispatcher.message(Command("admin"))
async def admin(message: Message) -> None:
    if message.from_user.id in bot_admins:
        translate_message(message)
        ru_text, en_text = translate_message(message=message)
        users: list = [i[0] for i in db.get_all_users_id()]
        for user in users:
            # Load user language.
            user_language: str = db.get_user_language(user_id=user)
            await bot.send_message(
                chat_id=user,
                text=ru_text if user_language == "ru" else en_text,
                reply_markup=mailing_keyboard(user_language))
        await message.answer("Рассылка отправлена.")
    return None


def translate_message(message: Message) -> tuple:
    text = message.text
    text_list: list = text.split("//")
    print(text_list)
    ru_text: str = text_list[0].split("\n$")[1]
    en_text: str = text_list[1]
    return ru_text, en_text