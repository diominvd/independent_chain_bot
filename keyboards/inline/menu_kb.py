from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import database
from keyboards.button_constructor import button


def menu_kb(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    strings: dict[str, dict] = {
        "invitation": {
            "ru": "\nПрисоединяйся к Independent Chain.\nНам важен каждый ⚡️",
            "en": "\nJoin the Independent Chain.\nEveryone is important to us ⚡️"
        }
    }

    language: str = database.get_user_language(user_id=event.from_user.id)
    referal_text: str = f"{strings['invitation'][language]}\nhttps://t.me/inch_coin_bot?start={event.from_user.id}"

    buttons: dict[str, list] = {
        "ru": [button(signature="👤 Профиль", callback="profile"),
               button(signature="💳 Кошелёк", callback="wallet"),
               button(signature="📚 Информация", callback="information"),
               button(signature="🛟 Поддержка", callback="support"),
               button(signature="♻️ Добыча", callback="mining"),
               button(signature="🎉 События", callback="events_menu"),
               InlineKeyboardButton(text="Пригласить друга", switch_inline_query=referal_text)],
        "en": [button(signature="👤 Profile", callback="profile"),
               button(signature="💳 Wallet", callback="wallet"),
               button(signature="📚 Information", callback="information"),
               button(signature="🛟 Support", callback="support"),
               button(signature="♻️ Mining", callback="mining"),
               button(signature="🎉 Events", callback="events_menu"),
               InlineKeyboardButton(text="Invite friend", switch_inline_query=referal_text)]
    }

    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[language][0], buttons[language][1])
    builder.row(buttons[language][2], buttons[language][3])
    builder.row(buttons[language][4], buttons[language][5])
    builder.row(buttons[language][6])
    return builder.as_markup()