from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.config import users_table


def keyboard(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="Собрать", callback_data="claim"),
            InlineKeyboardButton(text="Обновить", callback_data="mining"),
            InlineKeyboardButton(text="Улучшения", callback_data="upgrades"),
            InlineKeyboardButton(text="Усилители", url="https://getgems.io/collection/EQCwKU6XtfzfiT-7-tbzZI1zjkt1PBmYshkUQ05QPLDviMPG?filter=%7B%22saleType%22%3A%22fix_price%22%7D"),
            InlineKeyboardButton(text="Назад", callback_data="profile")
        ],
        "en": [
            InlineKeyboardButton(text="Claim", callback_data="claim"),
            InlineKeyboardButton(text="Refresh", callback_data="mining"),
            InlineKeyboardButton(text="Upgrade", callback_data="upgrades"),
            InlineKeyboardButton(text="Boosters", url="https://getgems.io/collection/EQCwKU6XtfzfiT-7-tbzZI1zjkt1PBmYshkUQ05QPLDviMPG?filter=%7B%22saleType%22%3A%22fix_price%22%7D"),
            InlineKeyboardButton(text="Back", callback_data="profile")
        ]
    }

    user_language: str = users_table.get_value("language", "user_id", event.from_user.id)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[user_language][0], buttons[user_language][1])
    builder.row(buttons[user_language][2], buttons[user_language][3])
    builder.row(buttons[user_language][4])
    return builder.as_markup()


def keyboard_upgrades(event: Message | CallbackQuery) -> InlineKeyboardMarkup:
    buttons: dict[str, list] = {
        "ru": [
            InlineKeyboardButton(text="⚙️ Улучшить реактор", callback_data="upgrade_reactor"),
            InlineKeyboardButton(text="🕑 Улучшить хранилище", callback_data="upgrade_storage"),
            InlineKeyboardButton(text="Назад", callback_data="mining")
        ],
        "en": [
            InlineKeyboardButton(text="⚙️ Upgrade reactor", callback_data="upgrade_reactor"),
            InlineKeyboardButton(text="🕑 Upgrade storage", callback_data="upgrade_storage"),
            InlineKeyboardButton(text="Back", callback_data="mining")
        ]
    }

    user_language: str = users_table.get_value("language", "user_id", event.from_user.id)
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(buttons[user_language][0])
    builder.row(buttons[user_language][1])
    builder.row(buttons[user_language][2])
    return builder.as_markup()