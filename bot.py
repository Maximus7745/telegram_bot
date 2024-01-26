import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from config import token, host, user, password, storage_name
from sql_storage import MySQLStorage
bot = Bot(token=token, parse_mode=ParseMode.HTML)
from handlers import form, form_reduct, start, question, forms_list
from handlers_admin import admin_bot_reduct, admin, admin_forms, admin_questions, admin_right, admin_spam, admin_statistic
async def main() -> None:
    storage = MySQLStorage(host, user, password, storage_name)
    dp = Dispatcher(storage=storage)
    dp.include_routers(admin_bot_reduct.router, admin.router, 
                       admin_forms.router, admin_questions.router, admin_right.router, 
                       admin_spam.router, admin_statistic.router, form.router, form_reduct.router,
                       question.router, forms_list.router, start.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())






