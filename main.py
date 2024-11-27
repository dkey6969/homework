import asyncio
import logging

from bot_config import bot, dp
from homework.start import start_router
from homework.dialog import dialog_router

async def main():
    dp.include_router(start_router)
    dp.include_router(dialog_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())