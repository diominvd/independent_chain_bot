from config import database, bot


async def send_mailing(text: dict) -> list:
    counter: dict[str, int] = {
        "successfully": 0,
        "unsuccessfully": 0
    }
    users: list = database.get_all_user_id()
    for user in users:
        language: str = database.get_user_language(user_id=user)
        try:
            await bot.send_message(chat_id=user, text=text[language])
        except:
            counter["unsuccessfully"] += 1
        else:
            counter["successfully"] += 1
    result: list = [len(users), counter["successfully"], counter["unsuccessfully"]]
    return result