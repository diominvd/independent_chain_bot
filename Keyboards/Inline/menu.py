from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def keyboard(user_id: int, language: str) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    names: dict = {
        "ru": ["👤 Профиль", "💰 Кошелёк", "ℹ Информация", "🛟 Поддержка", "✨ События", "Пригласить друга"],
        "en": ["👤 Profile", "💰 Wallet", "ℹ Information", "🛟 Support", "✨ Events", "Invite friend"]
    }
    strings: dict = {
        "ru": "\nПрисоединяйся к Independent Chain.\nНам важен каждый ⚡️",
        "en": "\nJoin the Independent Chain.\nEveryone is important to us ⚡️"
    }

    builder.row(
        InlineKeyboardButton(text=names[language][0], callback_data="profile"),
        InlineKeyboardButton(text=names[language][1], callback_data="wallet"))
    builder.row(
        InlineKeyboardButton(text=names[language][2], callback_data="information"),
        InlineKeyboardButton(text=names[language][3], callback_data="support"))
    builder.row(
        InlineKeyboardButton(text=names[language][4], callback_data="events"))
    referal_link: str = f"https://t.me/inch_coin_bot?start={user_id}"
    builder.row(
        InlineKeyboardButton(text=names[language][5], switch_inline_query=f"{strings[language]}\n{referal_link}"))
    return builder.as_markup()