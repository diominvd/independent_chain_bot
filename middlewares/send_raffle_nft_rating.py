import asyncio

from config import database, bot


async def timer() -> None:
    while True:
        await asyncio.sleep(21600)
        database.cursor.execute("""SELECT referals FROM nft_event ORDER BY referals DESC LIMIT 5""")
        rating: list = [i[0] for i in database.cursor.fetchall()]
        try:
            strings: dict[str, dict] = {
                "rating": {
                    "ru": f"Промежуточные результаты события ✨\n\n"
                          f"1️⃣ {rating[0]} приглашённых\n"
                          f"2️⃣ {rating[1]} приглашённых\n"
                          f"3️⃣ {rating[2]} приглашённых\n"
                          f"4️⃣ {rating[3]} приглашённых\n"
                          f"5️⃣ {rating[4]} приглашённых",
                    "en": f"Interim results of the event ✨\n\n"
                          f"1️⃣ {rating[0]} invited\n"
                          f"2️⃣ {rating[1]} invited\n"
                          f"3️⃣ {rating[2]} invited\n"
                          f"4️⃣ {rating[3]} invited\n"
                          f"5️⃣ {rating[4]} invited"
                }
            }
        except:
            strings: dict[str, dict] = {
                "rating": {
                    "ru": "Рейтинг еще не сформирован.",
                    "en": "The rating has not been formed yet."
                }
            }

        users: list = [i for i in database.get_all_user_id()]
        for user in users:
            language: str = database.get_user_language(user_id=user)
            try:
                await bot.send_message(
                    chat_id=user,
                    text=strings["rating"][language],
                )
            except:
                pass