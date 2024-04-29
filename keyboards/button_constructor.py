from aiogram.utils.keyboard import InlineKeyboardButton


def button(signature: str, url: str = None, callback: str = None) -> InlineKeyboardButton:
    if url is None:
        return InlineKeyboardButton(text=signature, callback_data=callback)
    elif callback is None:
        return InlineKeyboardButton(text=signature, url=url)