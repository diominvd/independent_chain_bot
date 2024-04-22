from mysql.connector import connect, Error

from vars import database_user, database_password


class Database:
    def __init__(self):
        # Create connection to database.
        self.connection = connect(host="localhost", user=database_user, password=database_password, database="independent_chain_bot")
        self.cursor = self.connection.cursor()

        self.cursor.execute("CREATE DATABASE IF NOT EXISTS independent_chain;")
        self.connection.commit()

        # Create default table.
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                project_id INT AUTO_INCREMENT PRIMARY KEY,
                telegram_id BIGINT NOT NULL,
                username VARCHAR(100),
                wallet VARCHAR(100),
                lang VARCHAR(2),
                balance INT NOT NULL,
                referals INT NOT NULL,
                registration_date DATE,
                inviter_id BIGINT NOT NULL)
        """)
        self.connection.commit()

    def create_user(self, telegram_id: int, username: str, lang: str, registration_date: str, inviter_id: int) -> bool:
        self.cursor.execute("""
            INSERT INTO users (telegram_id, username, lang, balance, referals, registration_date, inviter_id) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (telegram_id, username, lang, 100, 0, registration_date, inviter_id, ))
        self.connection.commit()
        return True

    def add_user_wallet(self, telegram_id: int, wallet_address: str) -> bool:
        self.cursor.execute("""
            UPDATE users SET wallet = %s WHERE telegram_id = %s
        """, (wallet_address, telegram_id, ))
        self.connection.commit()
        return True

    def check_user(self, telegram_id: int) -> bool:
        self.cursor.execute("""
                    SELECT telegram_id FROM users;
                """)
        users = self.cursor.fetchall()
        return True if (telegram_id,) in users else False

    def load_profile(self, telegram_id: int) -> list:
        self.cursor.execute("""
            SELECT project_id, telegram_id, wallet, balance, referals, registration_date FROM users WHERE telegram_id = %s;
        """, (telegram_id, ))
        return list(self.cursor.fetchall()[0])

    def add_referal(self, inviter_id: int) -> bool:
        self.cursor.execute("""
            UPDATE users
            SET referals = referals + 1, balance = balance + 50 WHERE telegram_id = %s
        """, (inviter_id, ))
        self.connection.commit()
        return True
