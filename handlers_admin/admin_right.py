
from filters import IsAdminFilter 
from aiogram import types, Router, F

from aiogram.enums import ParseMode


from aiogram.filters import Command, StateFilter
import kboard_admin
from text import db



router = Router()


@router.callback_query(IsAdminFilter(), 
                       kboard_admin.AdminCallbackFactory.filter(F.action == "rights_distribution"))
async def change_rights_distributionss_handler(callback: types.CallbackQuery):
    my_id = callback.from_user.id
    id_adms = db.get_all_admins_id()

    markup = get_list_admins(my_id , id_adms)
    await callback.message.edit_text("""Доброго времени суток, выберите id администротора, которого надо лишить прав""",
    reply_markup= markup, parse_mode=ParseMode.HTML)



@router.callback_query(IsAdminFilter(), 
                       kboard_admin.AdminCallbackFactory.filter(F.action == "del_adm"))
async def del_admin_handler(callback: types.CallbackQuery, 
                             callback_data: kboard_admin.AdminCallbackFactory): 
    await callback.message.delete()
    if(db.del_admin_by_id(callback_data.value)):
        await callback.message.answer("""Администратор успешно удалён""", reply_markup =types.ReplyKeyboardRemove(), 
                                  parse_mode=ParseMode.HTML)
    my_id = callback.from_user.id
    id_adms = db.get_all_admins_id()
    markup = get_list_admins(my_id , id_adms)
    await callback.message.answer("""Доброго времени суток, выберите id администротора, которого надо лишить прав""",
    reply_markup= markup, parse_mode=ParseMode.HTML)


def get_list_admins(my_id, id_adms):
    texts = list()
    actions = list()
    values = list()
    for id in id_adms:
        if(id != my_id):    
            texts.append(db.get_username(id))
            actions.append("del_adm")
            values.append(id)
    texts.append("Назад")
    actions.append("start")
    values.append(0)
    return kboard_admin.create_inline_keyboard_builder(texts, actions, values)