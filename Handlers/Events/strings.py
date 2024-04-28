def ru_events(*args) -> str:
    return (f"Запускаем конкурс на первую партию NFT от Independent Chain 💎\n\n"
            f"Всего будет 5 призовых мест:\n\n"
            f"1️⃣ Место - 1000 $tINCH\n"
            f"2️⃣ Место - Серебрянная NFT\n"
            f"3️⃣ Место - Золотая NFT\n"
            f"4️⃣ Место - Бронзовая NFT\n"
            f"5️⃣ Место - 500 $tINCH\n\n"
            f"Несколько раз в сутки бот будет присылать топ-5 без каких-либо имён. Просто цифры.\n\n"
            f"Места будут распределены исходя из количества приглашённых вами пользователей. Желаем удачи.")


def en_events(*args) -> str:
    return (f"We are launching a competition for the first batch of NFT from Independent Chain 💎\n\n"
            f"There will be 5 prizes in total:\n\n"
            f"1️⃣ Place - 1000 $tINCH\n"
            f"2️⃣ Place - Silver NFT\n"
            f"3️⃣ Place - Gold NFT\n"
            f"4️⃣ Place - Bronze NFT\n"
            f"5️⃣ Place - 500 $tINCH\n\n"
            f"Several times a day, the bot will send the top 5 without any names. Just numbers.\n\n"
            f"Places will be distributed based on the number of users you invited. We wish you good luck.")


def ru_top(*args) -> str:
    args = args[0]
    return (f"Промежуточные результаты события ✨\n\n"
            f"1️⃣ {args[0]} приглашённых\n"
            f"2️⃣ {args[1]} приглашённых\n"
            f"3️⃣ {args[2]} приглашённых\n"
            f"4️⃣ {args[3]} приглашённых\n"
            f"5️⃣ {args[4]} приглашённых")


def en_top(*args) -> str:
    args = args[0]
    return (f"Interim results of the event ✨\n\n"
            f"1️⃣ {args[0]} invited\n"
            f"2️⃣ {args[1]} invited\n"
            f"3️⃣ {args[2]} invited\n"
            f"4️⃣ {args[3]} invited\n"
            f"5️⃣ {args[4]} invited")


strings: dict = {
    "events": {
        "ru": ru_events,
        "en": en_events
    },
    "top": {
        "ru": ru_top,
        "en": en_top
    }
}