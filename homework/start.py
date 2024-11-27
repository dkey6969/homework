from aiogram import Router, F, types
from aiogram.filters import Command


start_router = Router()


@start_router.message(Command("/start"))
async def start(message: types.Message):
    name = message.from_user.first_name
    msg = f"привет {name}"
    await message.answer(msg)