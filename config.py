from aiogram import Bot, Dispatcher
import secrets
from database import database as database_file

from handlers.command import command_router
from handlers.callback import callback_router

bot: Bot = Bot(token=secrets.API_TOKEN, parse_mode="html")
dispatcher: Dispatcher = Dispatcher()
# Connect routers to dispatcher.
dispatcher.include_routers(command_router, callback_router)
database = database_file.Database()
event_database = database_file.EventTable()