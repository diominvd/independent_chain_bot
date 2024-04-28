from markdown import Markdown
def ru_alert(*args) -> str:
    return "Для использования бота подпишитесь на каналы проекта. После этого нажмите кнопку \"Проверить\"."


def en_alert(*args) -> str:
    return "To use the bot, subscribe to the project channels. After that, click \"Check\"."


def ru_start(*args) -> str:
    return \
        (f"Добро пожаловать в {Markdown.bold('Independent Chain')} - амбициозный проект, с грандиозными планами. "
         f"Этот бот поможет вам присоединиться к нашему сообществу и оставаться в курсе последних новостей. "
         f"Получите {Markdown.bold('100')} $tINCH за подписку на каналы проекта и начинайте приглашать друзей 🤑 "
         f"Ведь только вместе мы сможем добиться успеха. Получайте {Markdown.bold('50')} $tINCH "
         f"за каждого приглашённого друга 💸\n\nДля просмотра профиля воспользуйтесь командой /profile. "
         f"Для того, чтобы привязать свой Ton Space кошелёк воспользуйтесь кнопкой \"Кошелёк\".")


def en_start(*args) -> str:
    return \
        (f"Welcome to the {Markdown.bold('Independent Chain')}, an ambitious project with ambitious plans. "
         f"This bot will help you join our community and stay up to date with the latest news. "
         f"Get {Markdown.bold('100')} $tINCH for subscribing to the project channels and start inviting friends 🤑 "
         f"After all, only together we can succeed. Get {Markdown.bold('50')} $tINCH for each invited friend 💸\n\n"
         f"To view the profile, use the /profile command. "
         f"In order to link your Ton Space wallet, use the \"Wallet\" button.")


strings: dict = {
    "alert": {
        "ru": ru_alert,
        "en": en_alert
    },
    "start": {
        "ru": ru_start,
        "en": en_start
    }
}
