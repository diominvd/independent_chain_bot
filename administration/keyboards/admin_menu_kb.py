from aiogram.types import InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import database
from keyboards.button_constructor import button


def admin_menu_kb(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [button(signature="Рассылка", callback="mailing"),
               button(signature="Сообщение", callback="mail"),
               button(signature="Статистика", callback="statistics"),
               button(signature="Закрыть панель", callback="admin_exit")],
        "en": [button(signature="Mailing", callback="mailing"),
               button(signature="Message", callback="message"),
               button(signature="Statistic", callback="statistics"),
               button(signature="Close panel", callback="admin_exit")]
    }
    language: str = database.get_user_language(user_id=event.from_user.id)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[language][0], buttons[language][1])
    builder.row(buttons[language][2])
    builder.row(buttons[language][3])
    return builder.as_markup()