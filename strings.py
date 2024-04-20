strings: dict = {
    "/start": {
        "RU": "Привет",
        "EN": "Hello"
    },
    "/info": {
        "RU": "Информация",
        "EN": "Information"
    },
    "/links": {
        "RU": "Ссылки",
        "EN": "Links"
    },
    "/profile": {
        "RU": "Профиль",
        "EN": "Profile"
    },
    "/settings": {
        "RU": "Настройки",
        "EN": "Settings"
    }
}


def translate_answer(command: str, user_language: str) -> str:
    if command in list(strings.keys()):
        message_text: str = strings[command][user_language]
        return message_text
    else:
        return "Error"