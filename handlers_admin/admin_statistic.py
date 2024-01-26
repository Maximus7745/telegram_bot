from filters import IsAdminFilter 
from aiogram import types, Router, F


from aiogram.filters import Command, StateFilter
import kboard_admin

from text import db


router = Router()

@router.callback_query(IsAdminFilter(), 
                       kboard_admin.AdminCallbackFactory.filter(F.action == "statistics"))
async def spam_start_handler(callback: types.CallbackQuery, 
                             callback_data: kboard_admin.AdminCallbackFactory): 
    forms_count = db.get_count_forms_by_month()
    await callback.message.edit_text(f"В этом месяце поступило {forms_count} заявок", 
                                     reply_markup=kboard_admin.create_inline_keyboard_builder(["Назад"], ["start"], [0]))