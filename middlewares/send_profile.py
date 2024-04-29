from aiogram.types import Message, CallbackQuery

from config import database, bot
from keyboards.inline.menu_kb import menu_kb
from markdown import markdown
from utils.translator import translate


async def send_profile(event: Message | CallbackQuery) -> None:
    """
    profile_data structure:
        {
            'registration': str,
            'last_activity': str,
            'language': str,
            'project_id': int,
            'user_id': int,
            'inviter_id': int,
            'username': str',
            'wallet': str,
            'balance': float,
            'referals': int
        }
    """
    profile_data: dict = database.get_user(event.from_user.id)
    strings: dict[str, dict] = {
        "profile": {
            "ru": f"{markdown.bold('Привет,')} @{profile_data['username']} 👋\n"
                  f"{markdown.bold('Ваш UID')}: {profile_data['project_id']}\n"
                  f"{markdown.bold('Баланс')}: {profile_data['balance']} $tINCH\n"
                  f"{markdown.bold('Друзья')}: {profile_data['referals']}\n"
                  f"{markdown.bold('Ton Space')}: {markdown.monospaced(profile_data['wallet'])}\n\n"
                  f"{markdown.bold('Реферальная ссылка')}:\n"
                  f"{markdown.monospaced(f't.me/inch_coin_bot?start={profile_data['user_id']}')}\n"
                  f"(Нажмите, чтобы скопировать)",
            "en": f"{markdown.bold('Hello,')} @{profile_data['username']} 👋\n"
                  f"{markdown.bold('Your UID')}: {profile_data['project_id']}\n"
                  f"{markdown.bold('Balance')}: {profile_data['balance']} $tINCH\n"
                  f"{markdown.bold('Friends')}: {profile_data['referals']}\n"
                  f"{markdown.bold('Ton Space')}: {markdown.monospaced(profile_data['wallet'])}\n\n"
                  f"{markdown.bold('Referal link')}:\n"
                  f"{markdown.monospaced(f't.me/inch_coin_bot?start={profile_data['user_id']}')}\n"
                  f"(Click to copy)"
        },
        "update": {
            "ru": "Данные обновлены.",
            "en": "The data has been updated."
        }
    }

    if type(event).__name__ == "Message":
        await event.answer(
            text=translate(event, strings["profile"]),
            reply_markup=menu_kb(event),
        )
        await bot.delete_message(chat_id=event.from_user.id, message_id=event.message_id)
    elif type(event).__name__ == "CallbackQuery":
        try:
            await event.message.edit_text(
                text=translate(event, strings["profile"]),
                reply_markup=menu_kb(event)
            )
        except Exception as exc:
            await event.answer(text=translate(event, strings["update"]))
        else:
            await event.answer(text=translate(event, strings["update"]))
    return None