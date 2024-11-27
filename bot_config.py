from aiogram import Bot, Dispatcher
from dotenv import dotenv_values
from database.database import Database

config = dotenv_values(".env")
bot = Bot(token=config["BOT_TOKEN"])
dp = Dispatcher()
database = Database("database.sqlite")