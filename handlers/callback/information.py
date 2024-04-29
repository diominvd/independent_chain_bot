from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import database
from handlers.callback import callback_router
from keyboards.inline.infrormation_kb import information_kb
from utils.translator import translate


@callback_router.callback_query(F.data == "information")
@database.update_activity
async def information_callback(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "information": {
            "ru": f"$INCH - жетон , выпущенный в сети TON. Его цель - привлечь аудиторию в проект, которая в дальнейшем "
                  f"станет участниками Independent Chain. Всего было выпущено 10,000,000 $INCH 💸\n\n"
                  f"Баланс вашего профиля рассчитывается в $tINCH - внутрення валюта бота которая в последующем "
                  f"автоматически будет конвертирована в $INCH 🔄\n\n"
                  f"Для более подробного знакомства с проектом Independent Chain "
                  f"рекомендуем ознакомиться с Whitepaper проекта по ссылке ниже.",
            "en": f"$INCH is a token issued on the TON network. His goal is to attract an audience to the project, which "
                  f"will later become members of the Independent Chain. A total of 10,000,000 $INCH was issued 💸\n\n"
                  f"The balance of your profile is calculated in $tINCH - the internal currency of the bot, "
                  f"which will later be automatically converted to $INCH 🔄\n\n"
                  f"For a more detailed acquaintance with the Independent Chain project, we recommend that you "
                  f"read the project Whitepaper at the link below."
        }
    }

    await callback.answer(show_alert=False)
    await callback.message.edit_text(
        text=translate(callback, strings["information"]),
        reply_markup=information_kb(callback)
    )
    return None
