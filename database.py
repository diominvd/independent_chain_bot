from datetime import datetime
from mysql.connector import connect

from secret import db_name, db_user, db_password


class Database:
    def __init__(self):
        self.connection = connect(host="localhost", user=db_user, password=db_password, database=db_name)
        self.cursor = self.connection.cursor()

        # Create default table.
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    registration VARCHAR(20),
                    last_activity VARCHAR(20),
                    language VARCHAR(2),
                    project_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    inviter_id BIGINT,
                    username VARCHAR(100),
                    wallet VARCHAR(100),
                    balance FLOAT,
                    referals INT)
            """)
        self.connection.commit()

    def get_all_users_id(self) -> list:
        self.cursor.execute("""SELECT user_id FROM users""")
        return self.cursor.fetchall()

    def check_user_existence(self, telegram_id: int) -> bool:
        self.cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (telegram_id,))
        return False if not self.cursor.fetchall() else True

    def add_new_user(self, user_data: dict) -> bool:
        self.cursor.execute("""INSERT INTO users (registration, last_activity, language, user_id, username, balance, referals) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                            (user_data["registration"], user_data["last_activity"], user_data["language"], user_data["telegram_id"], user_data["username"], user_data["balance"], user_data["referals"],))
        self.connection.commit()
        return True

    def update_last_activity(self, user_id: int) -> bool:
        self.cursor.execute("""UPDATE users SET last_activity = %s WHERE user_id = %s""",
                            (str(datetime.now().strftime("%d.%m.%Y %H:%M:%S")), user_id))
        self.connection.commit()
        return True

    def check_user_inviter(self, user_id: int, inviter_id: int) -> bool:
        self.cursor.execute("""UPDATE users SET inviter_id = %s WHERE user_id = %s""", (inviter_id, user_id,))
        if user_id != inviter_id:
            self.cursor.execute("""UPDATE users SET balance = balance + 50, referals = referals + 1 WHERE user_id = %s""",
                                (inviter_id, ))
            self.connection.commit()
        return True

    def get_user_id_by_username(self, username: str) -> int:
        self.cursor.execute("""SELECT user_id FROM users WHERE username = %s""",
                            (username, ))
        return self.cursor.fetchall()[0][0]

    def get_user_language(self, user_id: int) -> str:
        self.cursor.execute("""SELECT language FROM users WHERE user_id = %s""",
                            (user_id, ))
        return self.cursor.fetchall()[0][0]

    def get_user_wallet(self, user_id: int) -> list:
        self.cursor.execute("""SELECT wallet FROM users WHERE user_id = %s""",
                            (user_id, ))
        return self.cursor.fetchall()

    def load_profile_data(self, user_id: int) -> list:
        self.cursor.execute("""SELECT username, project_id, balance, referals, wallet FROM users WHERE user_id = %s""",
                            (user_id, ))
        profile_data: list = list(self.cursor.fetchall()[0])
        return profile_data

    def update_wallet(self, user_id: int, wallet: str) -> bool:
        self.cursor.execute("""UPDATE users SET wallet = %s WHERE user_id = %s""",
                            (wallet, user_id))
        self.connection.commit()
        return True
