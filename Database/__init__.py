from getpass import getpass
from mysql.connector import connect, Error


connection = connect(host="localhost", user="", password="")
cursor = connection.cursor()
