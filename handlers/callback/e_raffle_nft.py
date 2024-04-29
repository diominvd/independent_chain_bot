from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import database
from handlers.callback import callback_router
from keyboards.inline.event_kb import event_kb
from keyboards.inline.events_kb import events_kb
from keyboards.inline.wallet_kb import wallet_kb
from states import BotStates, EventsStates
from utils.translator import translate


@callback_router.callback_query(StateFilter(EventsStates.events_menu), F.data == "raffle_nft")
@database.update_activity
async def raffle_nft__callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(EventsStates.raffle_nft)
    strings: dict[str, dict] = {
        "event_description": {
            "ru": f"Запускаем конкурс на первую партию NFT от Independent Chain 💎\n\n"
                  f"Всего будет 5 призовых мест:\n\n"
                  f"1️⃣ Место - 1000 $tINCH\n"
                  f"2️⃣ Место - Серебрянная NFT\n"
                  f"3️⃣ Место - Золотая NFT\n"
                  f"4️⃣ Место - Бронзовая NFT\n"
                  f"5️⃣ Место - 500 $tINCH\n\n"
                  f"Несколько раз в сутки бот будет присылать топ-5 без каких-либо имён. Просто цифры.\n\n"
                  f"Места будут распределены исходя из количества приглашённых вами пользователей. Желаем удачи.",
            "en": f"We are launching a competition for the first batch of NFT from Independent Chain 💎\n\n"
                  f"There will be 5 prizes in total:\n\n"
                  f"1️⃣ Place - 1000 $tINCH\n"
                  f"2️⃣ Place - Silver NFT\n"
                  f"3️⃣ Place - Gold NFT\n"
                  f"4️⃣ Place - Bronze NFT\n"
                  f"5️⃣ Place - 500 $tINCH\n\n"
                  f"Several times a day, the bot will send the top 5 without any names. Just numbers.\n\n"
                  f"Places will be distributed based on the number of users you invited. We wish you good luck."
        }
    }

    await callback.answer(show_alert=False)
    await callback.message.edit_text(
        text=translate(callback, strings["event_description"]),
        reply_markup=event_kb(callback)
    )
    return None