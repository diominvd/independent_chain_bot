from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime

from mysql.connector import connect
from secrets import database


class Database:
    def __init__(self):
        self.connection = connect(host="localhost", user=database["username"], password=database["password"], database=database["name"])
        self.cursor = self.connection.cursor()

        # Create table "users" in database.
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (registration VARCHAR(20), last_activity VARCHAR(20), language VARCHAR(2), project_id INT AUTO_INCREMENT PRIMARY KEY, user_id BIGINT NOT NULL, inviter_id BIGINT, username VARCHAR(100), wallet VARCHAR(100), balance FLOAT, referals BIGINT)""")
        self.connection.commit()
        # Create event table "nft_event" in database.
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS nft_event(user_id BIGINT NOT NULL, referals INT)""")
        self.connection.commit()

    def get_all_user_id(self) -> list:
        self.cursor.execute("""SELECT user_id FROM users""")
        id_list: list = [i[0] for i in self.cursor.fetchall()]
        return id_list

    def create_user(self, data: dict) -> bool:
        try:
            self.cursor.execute("""INSERT INTO users (registration, last_activity, language, user_id, inviter_id, username, balance, referals) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                                (data["registration"], data["registration"], data["language"], data["user_id"], data["inviter_id"], data["username"], 100, 0))
        except:
            return False
        else:
            self.connection.commit()
            # Check inviter an award accrual.
            if data["user_id"] != data["inviter_id"]:
                self.cursor.execute("""UPDATE users SET balance = balance + 50, referals = referals + 1 WHERE user_id = %s""",
                                    (data["inviter_id"],))
                self.connection.commit()
            return True

    def get_user(self, user_id: int) -> dict:
        self.cursor.execute("""SELECT * FROM users WHERE user_id = %s""",
                            (user_id,))
        user_data: tuple = self.cursor.fetchall()[0]
        # Create user dictionary with data from database.
        user: dict = {
            "registration": user_data[0],
            "last_activity": user_data[1],
            "language": user_data[2],
            "project_id": user_data[3],
            "user_id": user_data[4],
            "inviter_id": user_data[5],
            "username": user_data[6],
            "wallet": user_data[7],
            "balance": user_data[8],
            "referals": user_data[9]
        }
        return user

    def check_user(self, user_id: int) -> bool:
        self.cursor.execute("""SELECT username FROM users WHERE user_id = %s""",
                            (user_id,))
        try:
            username: str = self.cursor.fetchall()[0][0]
        except:
            return False
        else:
            return True

    def get_user_language(self, user_id: int = None, username: str = None) -> str | None:
        """
        You can get user language by user_id or username.
        It is necessary to specify the parameter name when passing the value to the function.
        """
        if user_id is None:
            self.cursor.execute("""SELECT language FROM users WHERE username = %s""",
                                (username,))
        elif username is None:
            self.cursor.execute("""SELECT language FROM users WHERE user_id = %s""",
                                (user_id, ))
        try:
            language: str = self.cursor.fetchall()[0][0]
        except:
            return None
        else:
            if language not in ["ru", "en"]:
                language: str = "en"
            return language

    def get_user_id(self, username: str) -> int | None:
        self.cursor.execute("""SELECT user_id FROM users WHERE username = %s""",
                            (username,))
        try:
            user_id: int = self.cursor.fetchall()[0][0]
        except:
            return None
        else:
            return user_id

    def get_username(self, user_id: int) -> str | None:
        self.cursor.execute("""SELECT username FROM users WHERE user_id = %s""",
                            (user_id, ))
        try:
            username: str = self.cursor.fetchall()[0][0]
        except:
            return None
        else:
            return username

    def get_wallet(self, user_id: int = None, username: str = None) -> str | None:
        """
        You can get user wallet address by user_id or username.
        It is necessary to specify the parameter name when passing the value to the function.
        """
        if user_id is None:
            self.cursor.execute("""SELECT wallet FROM users WHERE username = %s""",
                                (username,))
        elif username is None:
            self.cursor.execute("""SELECT wallet FROM users WHERE user_id = %s""",
                                (user_id, ))
        wallet: str = self.cursor.fetchall()[0][0]
        return wallet

    def update_wallet(self, user_id: int, wallet: str) -> bool:
        try:
            self.cursor.execute("""UPDATE users SET wallet = %s WHERE user_id = %s""",
                                (wallet, user_id))
        except:
            return False
        else:
            return True

    def update_activity(self, func) -> object:
        async def wrapper(event: Message | CallbackQuery, state: FSMContext):
            user_id = event.from_user.id
            time: str = str(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
            self.cursor.execute("""UPDATE users SET last_activity = %s WHERE user_id = %s""",
                                (time, user_id))
            self.connection.commit()
            return await func(event, state)
        return wrapper


class EventTable(Database):
    def __init__(self):
        super().__init__()

    def create_inviter(self, inviter_id: int) -> None:
        self.cursor.execute("""INSERT INTO nft_event (user_id, referals) VALUES (%s, 0)""",
                            (inviter_id, ))
        self.connection.commit()
        return None

    def check_inviter_existence(self, inviter_id: int) -> any:
        self.cursor.execute("""SELECT user_id FROM nft_event WHERE user_id = %s""",
                            (inviter_id,))
        check = self.cursor.fetchone()
        return check

    def update_participant(self, event) -> None:
        """
        Update user referals value in event table.
        """
        try:
            inviter_id = event.text.split(" ")[1]
        except:
            pass
        else:
            if self.check_inviter_existence(inviter_id) is None:
                self.create_inviter(inviter_id)
            if event.from_user.id != inviter_id:
                self.cursor.execute("""UPDATE nft_event SET referals = referals + 1 WHERE user_id = %s""",
                                    (inviter_id,))
                self.connection.commit()
            return None
