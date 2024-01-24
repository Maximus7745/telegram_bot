import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from config import host, user, password, database
import config
from handlers import start
from aiogram.fsm.storage.memory import MemoryStorage
from db import Database
from sql_storage import MySQLStorage
#db = Database()
bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
from hundlers_admin import admin_bot_reduct
async def main() -> None:
    storage = MySQLStorage(host, user, password, "storage_db")
    dp = Dispatcher(storage=storage)
    #bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp.include_routers(start.router, admin_bot_reduct.router)
    #db = Database()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())






