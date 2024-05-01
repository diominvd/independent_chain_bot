from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from administration.handlers import admin_router
from administration.keyboards.statistic_kb import statistics_kb
from administration.states import AdminStates
from config import database
from markdown import markdown
from utils.translator import translate


@admin_router.callback_query(StateFilter(AdminStates.admin_panel), F.data == "statistics")
async def mailing_ru(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminStates.statistics)
    await callback.answer(show_alert=False)

    database.cursor.execute("""SELECT COUNT(*) FROM users""")
    users: list = database.cursor.fetchone()[0]

    database.cursor.execute("""SELECT SUM(balance) FROM users""")
    balances: float = database.cursor.fetchone()[0]

    database.cursor.execute("""SELECT SUM(referals) FROM users""")
    referals: int = database.cursor.fetchone()[0]

    database.cursor.execute("""SELECT COUNT(*) FROM mining""")
    miners: int = database.cursor.fetchone()[0]

    database.cursor.execute("""SELECT COUNT(*) FROM nft_event""")
    event_users: list = database.cursor.fetchone()[0]

    strings: dict[str, dict] = {
        "statistics": {
            "ru": f"{markdown.bold('Статистика Independent Chain Bot.')}\n"
                  f"Всего пользователей: {users}\n"
                  f"Получено монет: {balances}\n"
                  f"Приглашено: {referals}\n"
                  f"Майнеров: {miners}\n\n"
                  f"В конкурсе участвуют: {event_users}",
            "en": f"{markdown.bold('Independent Chain Bot statistics.')}\n"
                  f"Total users: {users}\n"
                  f"Coins received: {balances}\n"
                  f"Invited: {referals}\n"
                  f"Miners: {miners}\n\n"
                  f"The competition involves: {event_users}"
        }
    }

    await callback.message.edit_text(
        text=translate(callback, strings["statistics"]),
        reply_markup=statistics_kb(callback)
    )
    return None