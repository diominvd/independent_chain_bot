from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import bot, dispatcher, database as db
import decorators as dec
from Keyboards.Inline import information_keyboard
from States.Default import DefaultStates
import Text as txt


@dispatcher.callback_query(F.data == "information")
@dec.update_last_activity
async def information(event: CallbackQuery, state: FSMContext) -> None:
    # Set information state.
    await state.set_state(DefaultStates.information)
    # Stop callback.
    await event.answer(show_alert=False)
    # Load user language.
    user_language: str = db.get_user_language(user_id=event.from_user.id)
    # Edit menu message.
    await bot.edit_message_text(
        text=txt.translate_text(s, "information", user_language, event.from_user.id),
        chat_id=event.from_user.id,
        message_id=event.message.message_id)
    # Add keyboard to message.
    await bot.edit_message_reply_markup(
        chat_id=event.from_user.id,
        message_id=event.message.message_id,
        reply_markup=information_keyboard(language=user_language))
    return None


def ru_information(*args) -> str:
    return \
        f"$INCH - жетон , выпущенный в сети TON. Его цель - привлечь аудиторию в проект, которая в дальнейшем станет участниками Independent Chain. Всего было выпущено 10,000,000 $INCH 💸\n\nБаланс вашего профиля рассчитывается в $tINCH - внутрення валюта бота которая в последующем автоматически будет конвертирована в $INCH 🔄\n\nДля более подробного знакомства с проектом Independent Chain рекомендуем ознакомиться с Whitepaper проекта по ссылке ниже."


def en_information(*args) -> str:
    return \
        f"$INCH is a token issued on the TON network. His goal is to attract an audience to the project, which will later become members of the Independent Chain. A total of 10,000,000 $INCH 💸\n\n was issued. The balance of your profile is calculated in $tINCH - the internal currency of the bot, which will later be automatically converted to $INCH 🔄\n\n For a more detailed acquaintance with the Independent Chain project, we recommend that you read the project Whitepaper at the link below."


s: dict = {
    "information": {
        "ru": ru_information,
        "en": en_information
    }
}
