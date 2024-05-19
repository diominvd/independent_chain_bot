from mysql.connector import connect
from core.secrets import DATABASE


class Database:
    host = DATABASE["host"]
    username = DATABASE["username"]
    password = DATABASE["password"]
    scheme = DATABASE["scheme"]

    connection = connect(host=host, user=username, password=password, database=scheme)
    cursor = connection.cursor()


class Table(Database):
    def __init__(self):
        pass

    def create(self, table_name: str, columns: dict[str, str]) -> None:
        columns: list = [f"{key} {value}" for key, value in columns.items()]

        query: str = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        self.cursor.execute(query)
        self.connection.commit()
        return None

    def insert(self, table_name: str, data: dict[str, any]) -> None:
        print(', '.join([column for column in data.keys()]))
        print(', '.join([str(value) for value in data.values()]))
        query: str = f"INSERT INTO {table_name} ({', '.join([column for column in data.keys()])}) VALUES ({', '.join([value for value in data.values()])})"
        self.cursor.execute(query)
        self.connection.commit()
        return None


class TestTable(Table):
    def __init__(self):
        super().__init__()
        self.name: str = "test_table"
        self.columns: dict = {
            "username": "VARCHAR(255)",
            "password": "VARCHAR(255)",
            "number": "INT"
        }
        self.create(self.name, self.columns)


test = TestTable()
data = {"username": "John", "password": "1", "number": 100}
print(', '.join(data.keys()))
test.insert("test_table", data)