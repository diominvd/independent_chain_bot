from aiogram.types import Message, CallbackQuery

from config import bot
from markdown import markdown
from utils.translator import translate


async def send_greeting(event: Message | CallbackQuery) -> None:
    strings: dict[str, dict] = {
        "greeting": {
            "ru": f"Добро пожаловать в {markdown.bold('Independent Chain')} - амбициозный проект, "
                  f"с грандиозными планами. Этот бот поможет вам присоединиться к нашему сообществу и оставаться "
                  f"в курсе последних новостей. Получите {markdown.bold('100')} $tINCH за подписку на каналы проекта "
                  f"и начинайте приглашать друзей 🤑 Ведь только вместе мы сможем добиться успеха. "
                  f"Получайте {markdown.bold('50')} $tINCH за каждого приглашённого друга 💸\n\n"
                  f"Для просмотра профиля воспользуйтесь командой /profile. Для того, чтобы привязать свой Ton Space "
                  f"кошелёк воспользуйтесь кнопкой \"Кошелёк\".",
            "en": f"Welcome to the {markdown.bold('Independent Chain')}, an ambitious project with ambitious plans. "
                  f"This bot will help you join our community and stay up to date with the latest news. "
                  f"Get {markdown.bold('100')} $tINCH for subscribing to the project channels and start inviting "
                  f"friends 🤑 After all, only together we can succeed. Get {markdown.bold('50')} $tINCH for each "
                  f"invited friend 💸\n\nTo view the profile, use the /profile command. In order to link your Ton Space "
                  f"wallet, use the \"Wallet\" button."
        }
    }
    await bot.send_message(
        chat_id=event.from_user.id,
        text=translate(event, strings["greeting"])
    )
    await bot.delete_message(chat_id=event.from_user.id, message_id=event.message_id)
    return None