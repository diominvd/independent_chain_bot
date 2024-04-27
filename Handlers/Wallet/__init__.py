def ru_request_wallet(*args) -> str:
    return f"Отправьте адрес кошелька в чат с ботом Ton Space, чтобы привязать его к профилю."


def en_request_wallet(*args) -> str:
    return f"Send the wallet address to the chat with the Ton Space bot to link it to your profile."


def ru_request_new_wallet(*args) -> str:
    return f"К вашему профилю уже привязан адрес кошелька Ton Space. Чтобы привязать новый - отправьте адрес кошелька в чат с ботом Ton Space."


def en_request_new_wallet(*args) -> str:
    return f"The Ton Space wallet address is already linked to your profile. To link a new one, send the wallet address to the chat with the Ton Space bot."


def ru_wallet_accepted(*args) -> str:
    return f"Адрес кошелька успешно привязан ✨"


def en_wallet_accepted(*args) -> str:
    return f"The wallet address has been successfully linked ✨"


strings: dict = {
    "no_wallet": {
        "ru": ru_request_wallet,
        "en": en_request_wallet
    },
    "yes_wallet": {
        "ru": ru_request_new_wallet,
        "en": en_request_new_wallet
    },
    "wallet_accepted": {
        "ru": ru_wallet_accepted,
        "en": en_wallet_accepted
    }
}