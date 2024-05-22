from aiogram import Bot, Dispatcher
from core.secrets import API_TOKEN
from database.field import Field
from database.table import UsersTable, MiningTable, UsersCodesTable, CodesTable

bot: Bot = Bot(token=API_TOKEN, parse_mode="html")
dispatcher: Dispatcher = Dispatcher()

UsersTable: UsersTable = UsersTable(
    name="users",
    project_id=Field("project_id", "BIGINT", "AUTO_INCREMENT PRIMARY KEY"),
    user_id=Field("user_id", "BIGINT"),
    username=Field("username", "VARCHAR(255)"),
    language=Field("language", "VARCHAR(2)"),
    wallet=Field("wallet", "VARCHAR(48)"),
    balance=Field("balance", "FLOAT"),
    referals=Field("referals", "BIGINT"),
)

MiningTable: MiningTable = MiningTable(
    name="mining",
    user_id=Field("user_id", "BIGINT"),
    username=Field("username", "VARCHAR(255)"),
    last_claim=Field("last_claimed", "BIGINT"),
    reactor=Field("reactor", "INT"),
    storage=Field("storage", "INT"),
    bot=Field("bot", "INT")
)

UserCodesTable: UsersCodesTable = UsersCodesTable(
    name="user_codes",
    user_id=Field("user_id", "BIGINT"),
    username=Field("username", "VARCHAR(255)"),
    last_code=Field("last_code", "DATETIME")
)

CodesTable: CodesTable = CodesTable(
    name="codes",
    code=Field("code", "VARCHAR(255)"),
    value=Field("value", "FLOAT"),
    activations=Field("activations", "INT")
)