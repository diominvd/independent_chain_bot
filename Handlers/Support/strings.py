def ru_support(*args) -> str:
    return \
        (f"В случае возникновения ошибок или каких-либо проблем с ботом просим написать вас в поддержку: @diominvdev.\n\n"
         f"Текущая версия бота: 2.3.1 🤖")


def en_support(*args) -> str:
    return \
        (f"In case of errors or any problems with the bot, please write to support: @diominvdev.\n\n"
         f"The current version of the bot is 2.3.1 🤖")


strings: dict = {
    "support": {
        "ru": ru_support,
        "en": en_support
    }
}
