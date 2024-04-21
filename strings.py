def translate_answer(command: str, user_language: str, *args) -> str:
    if command in list(strings.keys()):
        if user_language == "ru":
            message_text: str = strings[command]["ru"](*args)
        else:
            message_text: str = strings[command]["en"](*args)
        return message_text
    else:
        return "Error"


def translate_button(button: str, language: str) -> str:
    return buttons[button][language]


def ru_start(*args) -> str:
    text: str = (f"Добро пожаловать в Independent Chain Bot.\n\n"
                 f"<b>Список доступных команд:</b>\n"
                 f"/start - Перезапустить бота.\n"
                 f"/info - Краткая информация.\n"
                 f"/profile - Ваш профиль.\n"
                 f"/wallet - Привязать кошелёк.\n"
                 f"/links - Ссылки, связанные с проектом.\n"
                 f"/coin - Информация о жетоне.")
    return text


def en_start(*args) -> str:
    text: str = (f"Welcome to Independent Chain Bot.\n\n"
                 f"<b>List of available commands:</b>\n"
                 f"/start - Restart bot.\n"
                 f"/info - Brief information.\n"
                 f"/profile - Your profile.\n"
                 f"/wallet - Link your wallet.\n"
                 f"/links - Links related to the project.\n"
                 f"/coin - Information about the token.")
    return text


def ru_info(*args) -> str:
    text: str = (f"<b>Independent Chain (INCH)</b> - проект, запущенный группой энтузиастов. Основная цель - создание "
                 f"децентрализованной блокчейн сети в которой полностью отсутствует возможность группового или "
                 f"единоличного управления. Все решения, непосредственно связанные с изменениями в сети, будут приняты "
                 f"после достижения консенсуса между всеми участниками сети. Исходный код проекта полностью открыт. "
                 f"Из этого следует, что любой пользователь или начинающий разработчик сможет использовать сеть INCH "
                 f"для реализации и тестирования своих проектов на основе технологии блокчейн без необходимости "
                 f"написания сети с нуля. Данное решение откроет широкий спектр возможностей перед мало известными, "
                 f"но перспективными разработчиками.")
    return text


def en_info(*args) -> str:
    text: str = (f"<b>Independent Chain (INCH)</b> - a project launched by a group of enthusiasts. "
                 f"The main goal is to create a decentralized blockchain network in which "
                 f"there is no possibility of group or individual management. All decisions directly "
                 f"related to changes in the network will be made after reaching consensus among all "
                 f"network participants. The source code of the project is completely open. It follows "
                 f"that any user or novice developer will be able to use the INCH network to implement "
                 f"and test their projects based on blockchain technology without having to write a "
                 f"network from scratch. This solution will open up a wide range of opportunities for "
                 f"little-known, but promising developers.")
    return text


def ru_profile(*args) -> str:
    profile_data: list = args[0]
    date_values: list = str(profile_data[5]).split("-")
    date: str = f"{date_values[2]}-{date_values[1]}-{date_values[0]}"
    text: str = (f"<b>Ваш ID в проекте:</b> {profile_data[0]}\n"
                 f"<b>Адрес TON кошелька:</b> <code>{profile_data[2]}</code>\n"
                 f"<b>Баланс:</b> {profile_data[3]} INCH\n"
                 f"<b>Количество рефералов:</b> {profile_data[4]}\n"
                 f"<b>Дата регистрации:</b> {date}\n\n"
                 f"<b>Ваша реферальная ссылка:</b> <code>t.me/inch_coin_bot?start={profile_data[1]}</code>")
    return text


def en_profile(*args) -> str:
    profile_data: list = args[0]
    date: list = str(profile_data[5]).split("-")
    date: str = f"{date[2]}-{date[1]}-{date[0]}"
    text: str = (f"<b>Your ID in project:</b> {profile_data[0]}\n"
                 f"<b>TON wallet address:</b> <code>{profile_data[2]}</code>\n"
                 f"<b>Balance:</b> {profile_data[3]} INCH\n"
                 f"<b>Number of referrals:</b> {profile_data[4]}\n"
                 f"<b>Date of registration:</b> {date}\n\n"
                 f"<b>Your referral link:</b> <code>t.me/inch_coin_bot?start={profile_data[1]}</code>")
    return text


def ru_links(*args) -> str:
    text: str = (f"Канал проекта: @inch_coin\n"
                 f"Канал команды: @diominvdev\n"
                 f"Чат проекта: @diominvdevc\n\n"
                 f"Твиттер проекта: x.com/inch_coin\n\n:"
                 f"Исходный код проекта: clck.ru/3ACbjN\n"
                 f"Исходный код бота: clck.ru/3ACbju\n\n"
                 f"Whitepaper проекта: clck.ru/3ACbkk")
    return text


def en_links(*args) -> str:
    text: str = (f"Channel of the project: @inch_coin\n"
                 f"Channel of the team: @diominvdev\n"
                 f"Project Chat: @diominvdevc\n\n"
                 f"Twitter of project: x.com/inch_coin\n\n:"
                 f"Source code of the project: clck.ru/3ACbjN\n"
                 f"Source code of the bot: clck.ru/3ACbju\n\n"
                 f"Whitepaper of the project: clck.ru/3ACbmB")
    return text


def ru_coin(*args) -> str:
    text: str = (f"<b>Выпущено монет:</b> 10 000 000\n"
                 f"<b>Адрес контракта:</b> <code>EQDRaPxN8MkJOJYX-adlBBFnhMlHfPzIgD7NtyM0dtiauCZL</code>\n"
                 f"<b>Обзор на TONSCAN:</b> clck.ru/3ACbvj")
    return text


def en_coin(*args) -> str:
    text: str = (f"<b>Coins issued</b> - 10 000 000\n"
                 f"<b>Contract address</b> - <code>EQDRaPxN8MkJOJYX-adlBBFnhMlHfPzIgD7NtyM0dtiauCZL</code>\n"
                 f"<b>Review on TONSCAN</b> - clck.ru/3ACbvj")
    return text


def ru_subscribe(*args) -> str:
    text: str = f"Для использования бота подпишитесь на каналы проекта и перезапустите бота."
    return text


def en_subscribe(*args) -> str:
    text: str = f"To use the bot, subscribe to the project channels and restart bot."
    return text


def ru_wallet_request(*args) -> str:
    text: str = f"Отправьте адрес вашего TON кошелька. Будьте внимательны. Проверьте правильность адреса перед отправкой."
    return text


def en_wallet_request(*args) -> str:
    text: str = f"Send the address of your TON wallet. Be careful. Check that the address is correct before sending."
    return text


def ru_wallet_accept(*args) -> str:
    text: str = f"Кошелёк успешно сохранён."
    return text


def en_wallet_accept(*args) -> str:
    text: str = f"The wallet has been successfully saved."
    return text


def ru_wallet_accept_error(*args) -> str:
    text: str = f"Некорректный адрес кошелька."
    return text


def en_wallet_accept_error(*args) -> str:
    text: str = f"Incorrect address of wallet."
    return text


strings: dict = {
    "/start": {
        "ru": ru_start,
        "en": en_start
    },
    "/info": {
        "ru": ru_info,
        "en": en_info
    },
    "/profile": {
        "ru": ru_profile,
        "en": en_profile
    },
    "/links": {
        "ru": ru_links,
        "en": en_links
    },
    "/coin": {
        "ru": ru_coin,
        "en": en_coin
    },
    "subscribe": {
        "ru": ru_subscribe,
        "en": en_subscribe
    },
    "wallet_request": {
        "ru": ru_wallet_request,
        "en": en_wallet_request
    },
    "wallet_accept": {
        "ru": ru_wallet_accept,
        "en": en_wallet_accept
    },
    "wallet_accept_error": {
        "ru": ru_wallet_accept_error,
        "en": en_wallet_accept_error
    },
    "unknown": {
        "ru": 1,
        "en": 1
    }
}

buttons: dict = {
    "main_channel": {
        "ru": "Канал проекта",
        "en": "Project channel"
    },
    "dev_channel": {
        "ru": "Канала разработчиков",
        "en": "Developers channel"
    }
}
