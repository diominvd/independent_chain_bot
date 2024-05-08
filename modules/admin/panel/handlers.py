from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from modules import AdminModuleStates
from modules.admin import AdminModule
from core.config import users_table, bot
from markdown import Markdown
from translator import Translator


@AdminModule.router.message(Command("panel", "admin"))
@AdminModule.router.callback_query(F.data == "panel")
async def panel(event: Message | CallbackQuery, state: FSMContext) -> None:
    strings: dict[str, dict] = {
        "description": {
            "ru": f"{Markdown.bold('Администратор')}: @{event.from_user.username}\n"
                  f"Список разделов:\n"
                  f"• Сообщения - отправка сообщения пользователю, массовая рассылка.\n"
                  f"• База данных - статистика, получение значения, изменение значения\n\n"
                  f"Для закрытия панели нажмите соответсвующую кнопку.",
            "en": f"{Markdown.bold('Administrator')}: @{event.from_user.username}\n"
                  f"List of sections:\n"
                  f"• Messages - sending a message to the user, mass mailing.\n"
                  f"• Database - statistics, getting a value, changing a value\n\n"
                  f"To close the panel, press the corresponding button.",
        }
    }

    await state.set_state(AdminModuleStates.panel)

    match type(event).__name__:
        case "Message":
            await bot.delete_message(event.from_user.id, event.message_id)

            await event.answer(
                text=Translator.text(event, strings, "description"),
                reply_markup=AdminModule.modules["panel"].keyboard(event))

        case "CallbackQuery":
            await event.message.edit_text(
                text=Translator.text(event, strings, "description"),
                reply_markup=AdminModule.modules["panel"].keyboard(event))
    return None


@AdminModule.router.callback_query(F.data == "close_panel")
async def start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.delete()
    return None