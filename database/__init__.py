import datetime
from mysql.connector import connect

from core.secrets import DATABASE


class Database:
    connection = connect(
        host=DATABASE["host"],
        user=DATABASE["username"],
        password=DATABASE["password"],
        database=DATABASE["name"]
    )
    cursor = connection.cursor()

    @classmethod
    def create(cls, query: str, values: tuple = ()) -> None:
        cls.cursor.execute(query, values)
        cls.connection.commit()
        return None

    @classmethod
    def select(cls, query: str, values: tuple) -> list:
        cls.cursor.execute(query, values)
        response: list = cls.cursor.fetchall()
        return response

    @classmethod
    def insert(cls, query: str, values: tuple) -> None:
        cls.cursor.execute(query, values)
        cls.connection.commit()
        return None

    @classmethod
    def update(cls, query: str, values: tuple) -> None:
        cls.cursor.execute(query, values)
        cls.connection.commit()
        return None


class UsersTable(Database):
    def __init__(self):
        self.start_reward: float = 100.0
        self.referal_reward: float = 50.0
        self._create_table()

    def _create_table(self) -> None:
        query: str = "CREATE TABLE IF NOT EXISTS users (registration DATETIME, last_activity DATETIME, language VARCHAR(2), project_id INT AUTO_INCREMENT PRIMARY KEY, user_id BIGINT NOT NULL UNIQUE, inviter_id BIGINT, username VARCHAR(100), wallet VARCHAR(100), balance FLOAT, referals BIGINT)"
        self.create(query)
        return None

    def create_user(self, user_data: dict) -> None:
        query: str = "INSERT INTO users (registration, last_activity, language, user_id, inviter_id, username, balance, referals) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values: tuple = tuple(key for key in user_data.values())
        self.insert(query, values)
        # A reward for the one who invited.
        if user_data["inviter_id"] != 0:
            query: str = "UPDATE users SET balance = balance + %s, referals = referals + 1 WHERE user_id = %s"
            values = tuple([self.referal_reward, user_data["inviter_id"]])
            self.insert(query, values)
        return None

    def check_user(self, user_id: int) -> bool:
        query: str = "SELECT user_id FROM users WHERE user_id = %s"
        values: tuple = tuple([user_id])
        response = True if len(self.select(query, values)) > 0 else False
        return response

    def get_user(self, user_id: int) -> dict:
        query: str = "SELECT * FROM users WHERE user_id = %s"
        values: tuple = tuple([user_id])
        response: list = self.select(query, values)
        # Packing data into a dictionary.
        user_data: dict[str, any] = {
            "registration": response[0][0],
            "last_activity": response[0][1],
            "language": response[0][2],
            "project_id": response[0][3],
            "user_id": response[0][4],
            "inviter_id": response[0][5],
            "username": response[0][6],
            "wallet": response[0][7],
            "balance": response[0][8],
            "referals": response[0][9]
        }
        return user_data

    def get_value(self, flag: str, condition: str, value: any) -> any:
        query: str = f"SELECT {flag} FROM users WHERE {condition} = %s"
        values: tuple = tuple([value])
        response: any = self.select(query, values)[0][0]
        return response

    def get_all_users_id(self) -> list:
        query: str = "SELECT user_id FROM users"
        values: tuple = ()
        response: list = [i[0] for i in self.select(query, values)]
        return response

    def update_wallet(self, user_id: int, wallet: str) -> None:
        query: str = "UPDATE users SET wallet = %s WHERE user_id = %s"
        values: tuple = tuple([wallet, user_id])
        self.update(query, values)
        return None

    def update_last_activity(self, func) -> object:
        async def wrapper(*args, **kwargs):
            user_id: int = args[0].from_user.id
            time: datetime = datetime.datetime.now()
            query: str = "UPDATE users SET last_activity = %s WHERE user_id = %s"
            values: tuple = tuple([time, user_id])
            self.update(query, values)
            return await func(*args, **kwargs)
        return wrapper


class MiningTable(Database):
    def __init__(self):
        self.global_booster: float = 1.0
        self._create_table()

    def _create_table(self) -> None:
        query: str = "CREATE TABLE IF NOT EXISTS mining (user_id BIGINT NOT NULL, last_claim DATETIME, booster FLOAT, claims INT, amount FLOAT, FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE)"
        self.create(query)
        return None

    def create_user(self, user_id: int) -> None:
        query: str = "INSERT INTO mining (user_id, last_claim, booster, claims, amount) VALUES (%s, %s, %s, %s, %s)"
        values: tuple = tuple([user_id, datetime.datetime.now(), 1, 0, 0])
        self.insert(query, values)
        return None

    def check_user(self, user_id: int) -> bool:
        query: str = "SELECT user_id FROM mining WHERE user_id = %s"
        values: tuple = tuple([user_id])
        self.select(query, values)
        response: bool = True if len(self.select(query, values)) > 0 else False
        return response

    def get_user(self, user_id: int) -> list:
        query: str = "SELECT booster, claims, amount FROM mining WHERE user_id = %s"
        values: tuple = tuple([user_id])
        response: list = self.select(query, values)[0]
        return response

    def get_value(self, flag: str, condition: str, value: any) -> any:
        query: str = f"SELECT {flag} FROM mining WHERE {condition} = %s"
        values: tuple = tuple([value])
        response: any = self.select(query, values)[0][0]
        return response

    def get_last_claim(self, user_id: int) -> datetime:
        query: str = "SELECT last_claim FROM mining WHERE user_id = %s"
        values: tuple = tuple([user_id])
        time: datetime = self.select(query, values)[0][0]
        return time

    def update_booster(self, user_id: int, value: float) -> None:
        query: str = "UPDATE mining SET booster = %s WHERE user_id = %s"
        values: tuple = tuple([value, user_id])
        self.update(query, values)
        return None

    def claim(self, user_id: int, profit: float) -> None:
        query: str = "UPDATE mining SET claims = claims + 1, amount = amount + %s * %s WHERE user_id = %s"
        values: tuple = tuple([profit, self.global_booster, user_id])
        self.update(query, values)

        query: str = "UPDATE mining SET last_claim = %s WHERE user_id = %s"
        values: tuple = tuple([datetime.datetime.now(), user_id])
        self.update(query, values)

        query: str = "UPDATE users SET balance = balance + %s WHERE user_id = %s"
        values: tuple = tuple([profit, user_id])
        self.update(query, values)

        return None