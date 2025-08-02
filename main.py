import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from bot.handlers import user_handlers


async def main():
    load_dotenv()
    logging.basicConfig(level=logging.INFO)

    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        logging.error("BOT_TOKEN not found in .env file")
        return

    bot = Bot(token=bot_token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Register handlers
    dp.include_router(user_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
