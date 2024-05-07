from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.config import users_table


def keyboard(event: Message | CallbackQuery, wallet_connect: str) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="👤 Профиль", callback_data="profile"),
            InlineKeyboardButton(text="💳 Кошелек", url=wallet_connect, callback_data="wallet"),
            InlineKeyboardButton(text="🛟 Поддержка", callback_data="support"),
            InlineKeyboardButton(text="🔥 Добыча", callback_data="mining"),
            InlineKeyboardButton(text="🎉 События", callback_data="events"),
            InlineKeyboardButton(text="Пригласить друга", switch_inline_query=f"\nПрисоединяйся к Independent Chain.\nНам важен каждый ⚡️\nhttps://t.me/inch_coin_bot?start={event.from_user.id}"),
        ],
        "en": [
            InlineKeyboardButton(text="👤 Profile", callback_data="profile"),
            InlineKeyboardButton(text="💳 Wallet", url=wallet_connect, callback_data="wallet"),
            InlineKeyboardButton(text="🛟 Support", callback_data="support"),
            InlineKeyboardButton(text="🔥 Mining", callback_data="mining"),
            InlineKeyboardButton(text="🎉 Events", callback_data="events"),
            InlineKeyboardButton(text="Invite friend", switch_inline_query=f"\nJoin the Independent Chain.\nEveryone is important to us ⚡️\nhttps://t.me/inch_coin_bot?start={event.from_user.id}"),
        ]
    }

    user_language: str = users_table.get_value("language", "user_id", event.from_user.id)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[user_language][0], buttons[user_language][1])
    builder.row(buttons[user_language][2], buttons[user_language][3])
    builder.row(buttons[user_language][4])
    builder.row(buttons[user_language][5])
    return builder.as_markup()