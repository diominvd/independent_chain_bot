def translate_answer(command: str, user_language: str, *args) -> str:
    if command in list(strings.keys()):
        if user_language == "ru":
            message_text: str = strings[command]["ru"](*args)
        else:
            message_text: str = strings[command]["en"](*args)
        return message_text
    else:
        return "Error"


def ru_start(*args) -> str:
    text: str = (f"Добро пожаловать в Independent Chain Bot.\n\n"
                 f"Список доступных команд:\n"
                 f"/start - Рестарт бота.\n"
                 f"/info - Краткая информация.\n"
                 f"/profile - Ваш профиль.\n"
                 f"/links - Ссылки, связанные с проектом.\n"
                 f"/coin - Информация о жетоне.")
    return text


def en_start(*args) -> str:
    text: str = (f"Welcome to Independent Chain Bot.\n\n"
                 f"List of available commands:\n"
                 f"/start - Restart bot.\n"
                 f"/info - Brief information.\n"
                 f"/profile - Your profile.\n"
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
    text: str = (f"Ваш ID в проекте: {profile_data[0]}\n"
                 f"Баланс: {profile_data[1]}\n"
                 f"Количество рефералов: {profile_data[2]}\n"
                 f"Дата регистрации: {str(profile_data[3])}\n")
    return text


def en_profile(*args) -> str:
    profile_data: list = args[0]
    text: str = (f"Your ID in project: {profile_data[0]}\n"
                 f"Balance: {profile_data[1]}\n"
                 f"Number of referrals: {profile_data[2]}\n"
                 f"Date of registration: {str(profile_data[3])}\n")
    return text


def ru_links(*args) -> str:
    text: str = (f"Официальный канал проекта - @inch_coin\n"
                 f"Канал команды разработчиков - @diominvdev\n"
                 f"Чат проекта - @diominvdevc\n\n"
                 f"Исходный код проекта - clck.ru/3ACbjN\n"
                 f"Исходный код бота - clck.ru/3ACbju\n\n"
                 f"Whitepaper проекта - clck.ru/3ACbkk")
    return text


def en_links(*args) -> str:
    text: str = (f"The official channel of the project - @inch_coin\n"
                 f"The channel of the development team - @diominvdev\n"
                 f"Project Chat - @diominvdevc\n\n"
                 f"The source code of the project - clck.ru/3ACbjN\n"
                 f"The source code of the bot - clck.ru/3ACbju\n\n"
                 f"Whitepaper of the project - clck.ru/3ACbmB")
    return text


def ru_coin(*args) -> str:
    text: str = (f"Количество монет - 10 000 000\n"
                 f"Адрес контракта - <code>EQDRaPxN8MkJOJYX-adlBBFnhMlHfPzIgD7NtyM0dtiauCZL</code>\n"
                 f"Обзор на TONSCAN - clck.ru/3ACbvj")
    return text


def en_coin(*args) -> str:
    text: str = (f"Number of coins - 10 000 000\n"
                 f"Contract address - <code>EQDRaPxN8MkJOJYX-adlBBFnhMlHfPzIgD7NtyM0dtiauCZL</code>\n"
                 f"Review on TONSCAN - clck.ru/3ACbvj")
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
    "unknown": {
        "ru": 1,
        "en": 1
    }
}