def ru_check_error(*args) -> str:
    return "Проверка не пройдена."


def en_check_error(*args) -> str:
    return "The check is not passed."


def ru_check_success(*args) -> str:
    return "Проверка пройдена."


def en_check_success(*args) -> str:
    return "The check is passed."


strings: dict = {
    "check_error": {
        "ru": ru_check_error,
        "en": en_check_error
    },
    "check_success": {
        "ru": ru_check_success,
        "en": en_check_success
    }
}