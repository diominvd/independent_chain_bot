import asyncio

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import database, bot
from handlers.events import event_router
from keyboards.inline.event_kb import event_kb
from states import BotStates, EventsStates
from utils.translator import translate


@event_router.callback_query(StateFilter(BotStates.events_menu), F.data == "raffle_nft")
@database.update_activity
async def raffle_nft__callback(callback: CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "event_description": {
            "ru": f"Конкурс в честь запуска первой коллекции NFT от Independent Chain 💎\n\n"
                  f"Всего будет 5 призовых мест:\n\n"
                  f"1️⃣ Место - 1000 $tINCH\n"
                  f"2️⃣ Место - Серебрянная NFT\n"
                  f"3️⃣ Место - Золотая NFT\n"
                  f"4️⃣ Место - Бронзовая NFT\n"
                  f"5️⃣ Место - 500 $tINCH\n\n"
                  f"Несколько раз в сутки бот будет присылать актуальный рейтинг (первые 5 мест) с количеством приглашённых друзей.\n\n"
                  f"Места будут распределены исходя из количества приглашённых вами пользователей. Желаем удачи.",
            "en": f"Competition in honor of the launch of the first NFT collection from Independent Chain 💎\n\n"
                  f"There will be 5 prizes in total:\n\n"
                  f"1️⃣ Place - 1000 $tINCH\n"
                  f"2️⃣ Place - Silver NFT\n"
                  f"3️⃣ Place - Gold NFT\n"
                  f"4️⃣ Place - Bronze NFT\n"
                  f"5️⃣ Place - 500 $tINCH\n\n"
                  f"Several times a day, the bot will send an up-to-date rating (the first 5 places) with the number of invited friends.\n\n"
                  f"Places will be distributed based on the number of users you invited. We wish you good luck."
        }
    }

    await state.set_state(EventsStates.raffle_nft)
    await callback.answer(show_alert=False)
    await callback.message.edit_text(
        text=translate(callback, strings["event_description"]),
        reply_markup=event_kb(callback)
    )
    return None


async def timer() -> None:
    while True:
        await asyncio.sleep(21600)
        database.cursor.execute("""SELECT referals FROM nft_event ORDER BY referals DESC LIMIT 5""")
        rating: list = [i[0] for i in database.cursor.fetchall()]
        try:
            strings: dict[str, dict] = {
                "rating": {
                    "ru": f"Промежуточные результаты события ✨\n\n"
                          f"1️⃣ {rating[0]} приглашённых\n"
                          f"2️⃣ {rating[1]} приглашённых\n"
                          f"3️⃣ {rating[2]} приглашённых\n"
                          f"4️⃣ {rating[3]} приглашённых\n"
                          f"5️⃣ {rating[4]} приглашённых",
                    "en": f"Interim results of the event ✨\n\n"
                          f"1️⃣ {rating[0]} invited\n"
                          f"2️⃣ {rating[1]} invited\n"
                          f"3️⃣ {rating[2]} invited\n"
                          f"4️⃣ {rating[3]} invited\n"
                          f"5️⃣ {rating[4]} invited"
                }
            }
        except:
            strings: dict[str, dict] = {
                "rating": {
                    "ru": "Рейтинг еще не сформирован.",
                    "en": "The rating has not been formed yet."
                }
            }

        users: list = [i for i in database.get_all_user_id()]
        for user in users:
            language: str = database.get_user_language(user_id=user)
            try:
                await bot.send_message(
                    chat_id=user,
                    text=strings["rating"][language],
                )
            except:
                pass