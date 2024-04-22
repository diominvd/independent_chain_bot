from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import utils as u


def check_subscribe_keyboard(language: str):
    strings: dict = {
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
        [InlineKeyboardButton(text=u.translate_button(strings, "main", language), url="https://t.me/inch_coin")],
        [InlineKeyboardButton(text=u.translate_button(strings, "dev", language), url="https://t.me/diominvdev")],
        [InlineKeyboardButton(text=u.translate_button(strings, "check", language), callback_data="check_subscribe")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def main_keyboard(language: str):
    strings: dict = {
        "profile": {
            "ru": "Профиль",
            "en": "Profile"
        },
        "wallet": {
            "ru": "Кошелёк",
            "en": "Wallet"
        },
        "coin": {
            "ru": "Монета",
            "en": "Coin"
        },
        "links": {
            "ru": "Ссылки",
            "en": "Links"
        },
        "support": {
            "ru": "Поддержка",
            "en": "Support"
        }
    }
    buttons: list = [
        [
            InlineKeyboardButton(text=u.translate_button(strings, "profile", language), callback_data="profile"),
            InlineKeyboardButton(text=u.translate_button(strings, "wallet", language), callback_data="wallet")
        ],
        [
            InlineKeyboardButton(text=u.translate_button(strings, "coin", language), callback_data="coin"),
            InlineKeyboardButton(text=u.translate_button(strings, "links", language), callback_data="links")
        ],
        [InlineKeyboardButton(text=u.translate_button(strings, "support", language), callback_data="support")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
