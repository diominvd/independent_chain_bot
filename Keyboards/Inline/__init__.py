from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import Parse as parse
import Text as txt


def check_subscribe_keyboard(language: str) -> InlineKeyboardMarkup:
    s: dict = {
        "main": {
            "ru": "Канал проекта",
            "en": "Project channel"
        },
        "dev": {
            "ru": "Канал разработки",
            "en": "Dev channel"
        },
        "check": {
            "ru": "Проверить ✅",
            "en": "Check ✅"
        }
    }
    buttons: list = [
        [
            InlineKeyboardButton(text=txt.translate_button(s, "main", language), url="https://t.me/inch_coin")
        ],
        [
            InlineKeyboardButton(text=txt.translate_button(s, "dev", language), url="https://t.me/diominvdev")
        ],
        [
            InlineKeyboardButton(text=txt.translate_button(s, "check", language), callback_data="check_subscribe")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def main_keyboard(user_id: int, language: str) -> InlineKeyboardMarkup:
    def ru_share_text(*args) -> str:
        return f"Присоединяйся к Independent Chain.\nНам важен каждый ⚡️"

    def en_share_text(*args) -> str:
        return f"Join the Independent Chain.\nEveryone is important to us ⚡️"

    s: dict = {
        "profile": {
            "ru": "👤 Профиль",
            "en": "👤 Profile"
        },
        "wallet": {
            "ru": "💰 Кошелёк",
            "en": "💰 Wallet"
        },
        "information": {
            "ru": "ℹ Информация",
            "en": "ℹ Information"
        },
        "support": {
            "ru": "🛟 Поддержка",
            "en": "🛟 Support"
        },
        "events": {
            "ru": "✨ События",
            "en": "✨ Events"
        },
        "share": {
            "ru": "Пригласить друга",
            "en": "Invite friend"
        },
        "share_text": {
            "ru": ru_share_text,
            "en": en_share_text
        }
    }
    buttons: list = [
        [
            InlineKeyboardButton(text=txt.translate_button(s, "profile", language), callback_data="profile"),
            InlineKeyboardButton(text=txt.translate_button(s, "wallet", language), callback_data="wallet")
        ],
        [
            InlineKeyboardButton(text=txt.translate_button(s, "information", language), callback_data="information"),
            InlineKeyboardButton(text=txt.translate_button(s, "support", language), callback_data="support")
        ],
        [
            InlineKeyboardButton(text=txt.translate_button(s, "events", language), callback_data="events")
        ],
        [
            InlineKeyboardButton(text=txt.translate_button(s, "share", language), switch_inline_query=f"\n{txt.translate_text(s, "share_text", language)}\nt.me/inch_coin_bot?start={user_id}")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def mailing_keyboard(language: str) -> InlineKeyboardMarkup:
    s: dict = {
        "channel": {
            "ru": "Перейти на канал",
            "en": "Go to the channel"
        }
    }
    buttons: list = [
        [
            InlineKeyboardButton(text=txt.translate_button(s, "channel", language), url="https://t.me/inch_coin"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
