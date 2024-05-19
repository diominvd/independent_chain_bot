from mysql.connector import connect
from core.secrets import DATABASE


class Database:
    host = DATABASE["host"]
    user = DATABASE["user"]
    password = DATABASE["password"]
    scheme = DATABASE["scheme"]

    connection = connect(host=host, user=user, password=password, database=scheme)
    cursor = connection.cursor()


class Table(Database):
    def __init__(self):
        pass

    def create(self, table: tuple[str, dict]) -> bool:
        pass