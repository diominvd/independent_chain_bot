from aiogram import Bot, Dispatcher
import secrets
from administration.handlers import admin_router
from database import database as database_file

from handlers.command import command_router
from handlers.callback import callback_router
from handlers.events import event_router
from handlers.message import message_router

bot: Bot = Bot(token=secrets.API_TOKEN, parse_mode="html")
dispatcher: Dispatcher = Dispatcher()
dispatcher.include_routers(command_router, callback_router, message_router, event_router, admin_router)

database = database_file.Database()
event_database = database_file.EventTable()
mining_table = database_file.MiningTable()