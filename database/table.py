import datetime

from database.database import Database


class Table(Database):
    def __init__(self, name: str, **kwargs):
        self.name = name

        for title, field in kwargs.items():
            setattr(self, title, field)

        query: str = f"CREATE TABLE IF NOT EXISTS {self.name} ({', '.join([f'{field} {field_type.type}' for field, field_type in kwargs.items()])})"
        self.request(query, (), True)

    def select(self, fields: tuple, where: str = None, condition: any = None) -> any:
        query: str = f"SELECT {', '.join(fields) if len(fields) != 0 else '*'} FROM {self.name}"

        if where is not None:
            query += f" WHERE {where} = {condition if type(condition).__name__ != 'str' else f'\'{condition}\''}"

        self.request(query, (), False)

        if len(fields) == 0:
            return self.one()
        elif len(fields) == 1:
            response = self.one()
            if response is not None:
                return response[0]
            else:
                return None
        else:
            return self.all()

    def insert(self, **kwargs) -> None:
        query: str = f"INSERT INTO {self.name} ({', '.join([field for field in kwargs.keys()])}) VALUES ({', '.join([f'%s' for _ in range(len(kwargs))])})"
        self.request(query, tuple(value for value in kwargs.values()), True)

    def delete(self, where: str, condition: any) -> None:
        query: str = f"DELETE FROM {self.name} WHERE {where} = %s"
        self.request(query, (condition, ), True)

    def assign(self, field: str, value: any, where: str, condition: any) -> None:
        query: str = f"UPDATE {self.name} SET {field} = %s WHERE {where} = %s"
        self.request(query, (value, condition), True)

    def increase(self, field: str, value: float, where: str, condition: any) -> None:
        query: str = f"UPDATE {self.name} SET {field} = {field} + %s WHERE {where} = %s"
        self.request(query, (value, condition), True)

    def decrease(self, field: str, value: float, where: str, condition: any) -> None:
        query: str = f"UPDATE {self.name} SET {field} = {field} - %s WHERE {where} = %s"
        self.request(query, (value, condition), True)


class UsersTable(Table):
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)
        self.start: float = 100
        self.referal: float = 50

    def user(self, userid: int):
        class User:
            def __init__(self, uid, user_id, username, language, wallet, balance, referals):
                self.uid: int = uid
                self.user_id: int = user_id
                self.username: str = username
                self.language: str = language
                self.wallet: str = wallet
                self.balance: float = balance
                self.referals: int = referals

        data: tuple = self.select((), "user_id", userid)
        _user: User = User(*data)

        return _user


class MiningTable(Table):
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)
        self.booster: float = 1


class UsersCodesTable(Table):
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)

    def user(self, userid: int):
        class User:
            def __init__(self, user_id, username, last_code):
                self.user_id: int = user_id
                self.username: str = username
                self.last_code: datetime.datetime = last_code

        data: tuple = self.select((), "user_id", userid)
        _user: User = User(*data)

        return _user


class CodesTable(Table):
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)

    def get(self, signature: str):
        class Code:
            def __init__(self, code, value, activations):
                self.code: int = code
                self.value: float = value
                self.activations: int = activations

        data: tuple = self.select((), "code", signature)

        try:
            _code: Code = Code(*data)
        except:
            return None

        return _code

    def activate(self, code) -> None:
        if code.activations == 1:
            self.delete("code", code.code)
        else:
            self.decrease("activations", 1, "code", code.code)
        return None
