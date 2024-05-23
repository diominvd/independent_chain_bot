from database.database import Database


class Table(Database):
    def __init__(self, name: str, **kwargs):
        self.name = name

        for field, field_type in kwargs.items():
            setattr(self, field, field_type.type)

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
        print(query, (value for value in kwargs.values()))
        self.request(query, tuple(value for value in kwargs.values()), True)

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
        user: User = User(*data)

        return user

    def f_uid(self, where: str, condition: any) -> int:
        return self.select(("project_id", ), where, condition)

    def f_user_id(self, where: str, condition: any) -> int:
        return self.select(("user_id",), where, condition)

    def f_username(self, where: str, condition: any) -> str:
        return self.select(("user_id",), where, condition)

    def f_language(self, where: str, condition: any) -> str:
        return self.select(("language",), where, condition)

    def f_wallet(self, where: str, condition: any) -> str:
        return self.select(("wallet",), where, condition)

    def f_balance(self, where: str, condition: any) -> int:
        return self.select(("balance",), where, condition)

    def f_referals(self, where: str, condition: any) -> int:
        return self.select(("referals",), where, condition)


class MiningTable(Table):
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)
        self.booster: float = 1


class UsersCodesTable(Table):
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)


class CodesTable(Table):
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)