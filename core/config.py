from aiogram import Bot, Dispatcher
from core.secrets import API_TOKEN
from database import UsersTable, MiningTable, CodesTable

bot: Bot = Bot(token=API_TOKEN, parse_mode="html")
dispatcher: Dispatcher = Dispatcher()

users_table: UsersTable = UsersTable()
mining_table: MiningTable = MiningTable()
codes_table: CodesTable = CodesTable()