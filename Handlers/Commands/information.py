from aiogram import F
from aiogram.types import Message, CallbackQuery

from config import bot, dispatcher, database as db
from Keyboards.Inline import main_keyboard
import Parse as parse
import Text as txt


@dispatcher.callback_query(F.data == "information")
async def information(callback: CallbackQuery) -> None:
    # Update last user activity.
    db.update_last_activity(user_id=callback.from_user.id)
    # Load user language.
    user_language: str = db.get_user_language(user_id=callback.from_user.id)
    # Edit menu message.
    await bot.edit_message_text(
        text=txt.translate_text(s, "information", user_language, callback.from_user.id),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id)
    # Add keyboard to message.
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=main_keyboard(user_id=callback.from_user.id, language=user_language))
    return None


def ru_information(*args) -> str:
    return \
        f"$tINCH - жетон , выпущенный в сети TON. В дальнейшем может быть конвертирован в $INCH в Independent Chain.\n\n{parse.bold('Всего монет')}: 10 000 000 $INCH\n{parse.bold('Контракт')}: {parse.code('EQDRaPxN8MkJOJYX-adlBBFnhMlHfPzIgD7NtyM0dtiauCZL')}\n{parse.bold('TONSCAN')}: clck.ru/3ACbvj\n\nЧтобы оставаться в курсе последних новостей - подпишитесь на наши социальные сети:\n\n{parse.bold('Канал проекта')}: @inch_coin\n{parse.bold('Канал разработки')}: @diominvdev\n{parse.bold('Твиттер')}: x.com/inch_coin\n{parse.bold('Whitepaper')}: clck.ru/3ACbkk\n{parse.bold('Исходный код бота')}: clck.ru/3ACbju"""


def en_information(*args) -> str:
    return \
        f"$tINCH is a token issued on the TON network. In the future, it can be converted to $INCH in the Independent Chain.\n\n{parse.bold('Coins minted')}: 10 000 000 $INCH\n{parse.bold('Contract')}: {parse.code('EQDRaPxN8MkJOJYX-adlBBFnhMlHfPzIgD7NtyM0dtiauCZL')}\n\n{parse.bold('TONSCAN')}: clck.ru/3ACbvj\n\nTo stay up to date with the latest news, subscribe to our social networks:\n\n{parse.bold('Project channel')}: @inch_coin\n{parse.bold('Dev channel')}: @diominvdev\n{parse.bold('Twitter')}: x.com/inch_coin\n{parse.bold('Whitepaper')}: clck.ru/3ACbkk\n{parse.bold('Bot source code')}: clck.ru/3ACbju"


s: dict = {
    "information": {
        "ru": ru_information,
        "en": en_information
    }
}
