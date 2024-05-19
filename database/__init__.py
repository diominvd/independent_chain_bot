import datetime
import random

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

    @classmethod
    def delete(cls, query: str, values: tuple) -> None:
        cls.cursor.execute(query, values)
        cls.connection.commit()
        return None


class UsersTable(Database):
    def __init__(self):
        self.start_reward: float = 100.0
        self.referal_reward: float = 50.0
        self._create_table()

    def _create_table(self) -> None:
        query: str = "CREATE TABLE IF NOT EXISTS users (registration DATETIME, last_activity DATETIME, language VARCHAR(2), project_id INT AUTO_INCREMENT PRIMARY KEY, user_id BIGINT NOT NULL UNIQUE, inviter_id BIGINT, username VARCHAR(100), wallet VARCHAR(100), balance FLOAT, referals BIGINT, codes INT NOT NULL, last_code_activate DATETIME)"
        self.create(query)
        return None

    def create_user(self, user_data: dict) -> None:
        query: str = "INSERT INTO users (registration, last_activity, language, user_id, inviter_id, username, balance, referals, codes, last_code_activate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values: tuple = tuple(key for key in user_data.values())
        self.insert(query, values)
        # A reward for the one who invited.
        if user_data["inviter_id"] != 0:
            query: str = "UPDATE users SET balance = balance + %s, referals = referals + 1 WHERE user_id = %s"
            values = tuple([self.referal_reward, user_data["inviter_id"]])
            self.insert(query, values)
        return None

    def get_user(self, user_id: int) -> dict:
        query: str = "SELECT * FROM users WHERE user_id = %s"
        values: tuple = tuple([user_id])
        response: list = self.select(query, values)

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
            "referals": response[0][9],
            "codes": response[0][10],
            "last_code_activate": response[0][11]
        }
        return user_data

    def get_users_id(self) -> list:
        query: str = "SELECT user_id FROM users"
        values: tuple = ()
        response: list = [i[0] for i in self.select(query, values)]
        return response

    def get_last_code_activate(self, user_id: int) -> tuple:
        query: str = "SELECT last_code_activate FROM users WHERE user_id = %s"
        values: tuple = tuple([user_id])
        response: tuple = self.select(query, values)[0]
        return response

    def get_value(self, flag: str, condition: str, value: any) -> any:
        query: str = f"SELECT {flag} FROM users WHERE {condition} = %s"
        values: tuple = tuple([value])

        response: any = self.select(query, values)
        if len(response) != 0:
            response: list = [list(row) for row in response]
            return response[0][0]
        else:
            return False

    def check_user_existence(self, user_id: int) -> bool:
        query: str = "SELECT user_id FROM users WHERE user_id = %s"
        values: tuple = tuple([user_id])

        response = self.select(query, values)
        if len(response) != 0:
            return True
        else:
            return False

    def update_username(self, user_id: int, username: str) -> None:
        query: str = "UPDATE users SET username = %s WHERE user_id = %s"
        values: tuple = tuple([username, user_id])
        self.update(query, values)
        return None

    def update_balance(self, user_id: int, operation: str, value: float) -> None:
        query: str = f"UPDATE users SET balance = balance {operation} %s WHERE user_id = %s"
        values: tuple = tuple([value, user_id])
        self.update(query, values)
        return None

    def update_wallet(self, user_id: int, wallet: str) -> None:
        query: str = "UPDATE users SET wallet = %s WHERE user_id = %s"
        values: tuple = tuple([wallet, user_id])
        self.update(query, values)
        return None

    def activate_code(self, user_id: int, value: float) -> None:
        query: str = "UPDATE users SET codes = codes + 1, last_code_activate = %s, balance = balance + %s WHERE user_id = %s"
        values: tuple = tuple([datetime.datetime.now(), value, user_id])
        self.update(query, values)
        return None

    def update_last_activity(self, func) -> object:
        async def wrapper(event, state):
            user_id = event.from_user.id
            time: datetime = datetime.datetime.now()
            query: str = "UPDATE users SET last_activity = %s WHERE user_id = %s"
            values: tuple = tuple([time, user_id])
            self.update(query, values)
            return await func(event, state)
        return wrapper


class MiningTable(Database):
    def __init__(self):
        self.full_storage: list = []
        self.global_booster: float = 1.0
        self.upgrade_discount = 0
        self._create_table()

    def _create_table(self) -> None:
        query: str = "CREATE TABLE IF NOT EXISTS mining (user_id BIGINT NOT NULL, last_claim DATETIME, reactor INT, storage INT, bot BOOL NOT NULL, booster FLOAT, claims INT, amount FLOAT, FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE)"
        self.create(query)
        return None

    def create_user(self, user_id: int) -> None:
        query: str = "INSERT INTO mining (user_id, last_claim, reactor, storage, bot, booster, claims, amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values: tuple = tuple([user_id, datetime.datetime.now(), 1, 1, False, 1, 0, 0])
        self.insert(query, values)
        return None

    def check_user(self, user_id: int) -> bool:
        query: str = "SELECT user_id FROM mining WHERE user_id = %s"
        values: tuple = tuple([user_id])
        self.select(query, values)
        response: bool = True if len(self.select(query, values)) > 0 else False
        return response

    def get_user(self, user_id: int) -> list:
        query: str = "SELECT reactor, storage, bot, booster, claims, amount FROM mining WHERE user_id = %s"
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

    def update_reactor(self, user_id: int) -> None:
        query: str = "UPDATE mining SET reactor = reactor + 1 WHERE user_id = %s"
        values: tuple = tuple([user_id])
        self.update(query, values)
        return None

    def update_storage(self, user_id: int) -> None:
        query: str = "UPDATE mining SET storage = storage + 1 WHERE user_id = %s"
        values: tuple = tuple([user_id])
        self.update(query, values)
        return None

    def update_booster(self, user_id: int, value: float) -> None:
        query: str = "UPDATE mining SET booster = %s WHERE user_id = %s"
        values: tuple = tuple([value, user_id])
        self.update(query, values)
        return None

    def claim(self, user_id: int, profit: float) -> None:
        try:
            self.full_storage.remove(user_id)
        except:
            pass

        query: str = "UPDATE mining SET claims = claims + 1, amount = amount + %s * %s WHERE user_id = %s"
        values: tuple = tuple([profit, self.global_booster, user_id])
        self.update(query, values)

        query: str = "UPDATE mining SET last_claim = %s WHERE user_id = %s"
        values: tuple = tuple([datetime.datetime.now(), user_id])
        self.update(query, values)

        query: str = "UPDATE users SET balance = balance + %s * %s WHERE user_id = %s"
        values: tuple = tuple([profit, self.global_booster, user_id])
        self.update(query, values)

        return None


class CodesTable(Database):
    def __init__(self):
        self.symbols: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz"
        self._create_table()

    def _create_table(self) -> None:
        query: str = "CREATE TABLE IF NOT EXISTS codes (code_id BIGINT PRIMARY KEY AUTO_INCREMENT, code VARCHAR(20), activations INT, value FLOAT)"
        self.create(query)
        return None

    def generate(self, number: int, value: float) -> str:
        code_symbols: list = [random.choice(self.symbols) for i in range(16)]
        code: str = "".join(code_symbols)
        query: str = "INSERT INTO codes (code, activations, value) VALUES (%s, %s, %s)"
        values: tuple = tuple([code, number, value])
        self.insert(query, values)
        return code

    def update_code(self, code: str) -> bool:
        query: str = "SELECT activations FROM codes WHERE code = %s"
        activations: int = self.select(query, (code, ))[0][0]

        if activations > 0:
            query: str = "UPDATE codes SET activations = activations - 1 WHERE code = %s"
            self.update(query, (code, ))
            if activations == 1:
                self.delete_code(code)
                return True
            else:
                return True
        else:
            return False

    def load_code(self, code: str) -> list:
        query: str = "SELECT * FROM codes WHERE code = %s"
        values: tuple = tuple([code])
        code_data: list = self.select(query, values)
        return code_data

    def delete_code(self, code: str) -> None:
        query: str = "DELETE FROM codes WHERE code = %s"
        values: tuple = tuple([code])
        self.delete(query, values)
        return None