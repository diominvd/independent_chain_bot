from aiogram import Bot, Dispatcher
from vars import API_TOKEN
from Database import Database


bot: Bot = Bot(token=API_TOKEN, parse_mode="HTML")
dispatcher: Dispatcher = Dispatcher()
database = Database()