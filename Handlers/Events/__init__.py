def ru_events(*args) -> str:
    return \
        f"Запускаем конкурс на первую партию NFT от Independent Chain. Всего будет 5 призовых мест:\n\n1️⃣ Место - 1000 $tINCH\n2️⃣ Место - Серебрянная NFT\n3️⃣ Место - Золотая NFT\n4️⃣ Место - Бронзовая NFT\n5️⃣ Место - 500 $tINCH\n\nНесколько раз в сутки бот будет присылать топ-5 без каких-либо имён. Просто цифры.\n\nМеста будут распределены исходя из количества приглашённых вами пользователей. Желаем удачи."


def en_events(*args) -> str:
    return \
        f"We are launching a competition for the first batch of NFT from Independent Chain. There will be 5 prizes in total:\n\n1️⃣ Place - 1000 $tINCH\n2️⃣ Place - Silver NFT\n3️⃣ Place - Gold NFT\n4️⃣ Place - Bronze NFT\n5️⃣ Place - 500 $tINCH\n\nSeveral times a day, the bot will send the top 5 without any names. Just numbers.\n\nPlaces will be distributed based on the number of users you invited. We wish you good luck."


def ru_top(*args) -> str:
    args = args[0]
    return f"Промежуточные результаты события ✨\n\n1️⃣ {args[0]} приглашённых\n2️⃣ {args[1]} приглашённых\n3️⃣ {args[2]} приглашённых\n4️⃣ {args[3]} приглашённых\n5️⃣ {args[4]} приглашённых"


def en_top(*args) -> str:
    args = args[0]
    return f"Interim results of the event ✨\n\n1️⃣ {args[0]} invited\n2️⃣ {args[1]} invited\n3️⃣ {args[2]} invited\n4️⃣ {args[3]} invited\n5️⃣ {args[4]} invited"


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