from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from administration.keyboards.admin_menu_kb import admin_menu_kb
from administration.states import AdminStates
from config import database, bot
from markdown import markdown
from utils.translator import translate


async def send_admin_panel(event: Message | CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(AdminStates.admin_panel)
    strings: dict[str, dict] = {
        "description": {
            "ru": f"{markdown.bold('Администратор:')} @{database.get_username(event.from_user.id)}\n"
                  f"Список доступных действий:\n"
                  f"• Рассылка - отправить рассылку всем пользователям бота.\n"
                  f"• Сообщение - отправить сообщение конкретному пользователю.\n"
                  f"• Статистика - просмотр актуальной статистики бота.\n\n"
                  f"Для закрытия панели нажмите кнопку 'Закрыть панель'.",
            "en": f"{markdown.bold('Administrator:')} @{database.get_username(event.from_user.id)}\n"
                  f"List of available actions:\n"
                  f"• Newsletter - send a newsletter to all users of the bot.\n"
                  f"• Message - send a message to a specific user.\n"
                  f"• Statistics - view the current statistics of the bot.\n\n"
                  f"To close the panel, click the 'Close Panel' button."
        }
    }

    if type(event).__name__ == "Message":
        await event.answer(
            text=translate(event, strings["description"]),
            reply_markup=admin_menu_kb(event),
        )
    elif type(event).__name__ == "CallbackQuery":
        try:
            await event.message.edit_text(
                text=translate(event, strings["description"]),
                reply_markup=admin_menu_kb(event)
            )
        except Exception as exc:
            pass
    return None
