def ru_information(*args) -> str:
    return \
        f"$INCH - жетон , выпущенный в сети TON. Его цель - привлечь аудиторию в проект, которая в дальнейшем станет участниками Independent Chain. Всего было выпущено 10,000,000 $INCH 💸\n\nБаланс вашего профиля рассчитывается в $tINCH - внутрення валюта бота которая в последующем автоматически будет конвертирована в $INCH 🔄\n\nДля более подробного знакомства с проектом Independent Chain рекомендуем ознакомиться с Whitepaper проекта по ссылке ниже."


def en_information(*args) -> str:
    return \
        f"$INCH is a token issued on the TON network. His goal is to attract an audience to the project, which will later become members of the Independent Chain. A total of 10,000,000 $INCH 💸\n\n was issued. The balance of your profile is calculated in $tINCH - the internal currency of the bot, which will later be automatically converted to $INCH 🔄\n\n For a more detailed acquaintance with the Independent Chain project, we recommend that you read the project Whitepaper at the link below."


strings: dict = {
    "information": {
        "ru": ru_information,
        "en": en_information
    }
}