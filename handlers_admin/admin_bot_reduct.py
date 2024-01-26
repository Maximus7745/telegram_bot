from filters import IsAdminFilter 
from aiogram import types, Router, F

from aiogram.enums import ParseMode
from states import StatesReductBtn, StatesReductMsg, StateAddBtn, StatesReductForm
from bot import bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
import kboard_admin
from text import db, get_text, get_action_msg, get_button_name
import text

from kboard import get_reply_markup
import kboard

router = Router()






@router.callback_query(IsAdminFilter(), 
                       kboard_admin.AdminCallbackFactory.filter(F.action == "reduct"))
async def start_reduct_bot_handler(callback: types.CallbackQuery):
    markup = kboard_admin.start_reduct_bot_markup
    await callback.message.edit_text("""Раздел редактирования бота делится на два подраздела. Редактирование меню включает в себя редактировние стартового меню, которое видят пользователи при взаимодействии с ботом, а также изменение и добавление частозадаваемых вопросов. Редактировние формы же предполагает непосредственно изменение текста при заполнении пользователями формы для обучения.""", 
    reply_markup= markup, parse_mode=ParseMode.HTML)

@router.callback_query(IsAdminFilter(), 
                       kboard_admin.AdminCallbackFactory.filter(F.action == "select_lang"))
async def check_list_lang_reduct_handler(callback: types.CallbackQuery):
    await callback.message.edit_text("Select your language", 
                                     reply_markup= kboard_admin.lang_marup, parse_mode=ParseMode.HTML)

@router.callback_query(IsAdminFilter(), 
                       kboard_admin.AdminCallbackFactory.filter(F.action == "lang"))
async def select_lang_reduct_handler(callback: types.CallbackQuery, 
                             callback_data: kboard_admin.AdminCallbackFactory):
    lang = callback_data.string
    user_id = callback.from_user.id
    db.update_lang(user_id, lang)
    await start_reduct_bot_handler(callback)
@router.callback_query(IsAdminFilter(), 
                       kboard_admin.AdminCallbackFactory.filter(F.action == "refrash_tables"))
async def refrash_table(callback: types.CallbackQuery):
    if(db.del_buttons_lists()):
        db.create_buttons_lists()
    if(db.del_text()):
        db.create_text()
    if(db.del_menus()):
        db.create_menus()
    db.try_load_start_data()
    text.text = db.get_text()
    text.buttons_list = db.get_buttons_list()
    text.menus = db.get_menus_text()
    await callback.message.delete()
    await callback.message.answer("Все разделы бота ббыли успешно сброшены до изначальных")
    markup = kboard_admin.start_reduct_bot_markup
    await callback.message.answer("""Раздел редактирования бота делится на два подраздела. Редактирование меню включает в себя редактировние стартового меню, которое видят пользователи при взаимодействии с ботом, а также изменение и добавление частозадаваемых вопросов. Редактировние формы же предполагает непосредственно изменение текста при заполнении пользователями формы для обучения.""", 
    reply_markup= markup, parse_mode=ParseMode.HTML)



#редактирование меню
@router.callback_query(IsAdminFilter(), 
                    kboard_admin.AdminCallbackFactory.filter(F.action == "action"), 
                    kboard_admin.AdminCallbackFactory.filter(F.value == 1))
async def reduct_menu_start_hundler(callback: types.CallbackQuery, 
                             callback_data: kboard_admin.AdminCallbackFactory):
    user_id = callback.from_user.id
    lang = db.get_lang(user_id)

    markup = kboard_admin.get_action_menus(1, lang)
    await callback.message.edit_text(f"""Текст сообщения:{get_action_msg(0,lang)}""", 
                                     reply_markup= markup)

@router.message(StatesReductMsg.reduct_msg, F.text.lower() == "отмена")
@router.message(StatesReductBtn.reduct_btn, F.text.lower() == "отмена")
@router.message(StateAddBtn.add_btn, F.text.lower() == "отмена")
@router.message(StateAddBtn.add_msg, F.text.lower() == "отмена")
async def cancel_reduct_menus(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    user_data = await state.get_data()
    action_id = user_data["action_id"]
    await state.clear()
    await message.answer("""Отмена прошла успешно.""", reply_markup =types.ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)

    markup = kboard_admin.get_action_menus(action_id,lang)
    await message.answer(f"""Текст сообщения:{get_action_msg(action_id - 1, lang)} \n Текст кнопки: {get_button_name("action" + str(action_id), lang)}"""
                                     , reply_markup= markup)



#reduct_msg
@router.callback_query(IsAdminFilter(), 
                       kboard_admin.AdminCallbackFactory.filter(F.action == "reduct_msg"))
async def reduct_msg_handler(callback: types.CallbackQuery, 
                             callback_data: kboard_admin.AdminCallbackFactory, state: FSMContext): 
    user_id = callback.from_user.id
    lang = db.get_lang(user_id)
    action_id = callback_data.value
    await callback.message.delete()
    await callback.message.answer(f"Старый текст:{get_action_msg(action_id, lang)}. Введите новый текст сообщения.")
    await state.update_data(action_id=action_id)
    await state.set_state(StatesReductMsg.reduct_msg)


@router.message(StatesReductMsg.reduct_msg)
async def reduct_msg_text_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    user_data = await state.get_data()
    action_id = user_data["action_id"]
    msg = message.text
    db.update_message(action_id, msg, lang)

    text.menus = db.get_menus_text()
    # kboard_admin.menu_dict = kboard_admin.getMenues()
    # kboard.menu_dict = kboard.getMenues()
    await state.clear()
    markup = kboard_admin.get_action_menus(action_id,lang)
    await message.answer(f"""Текст сообщения:{get_action_msg(action_id - 1, lang)} \n Текст кнопки: {get_button_name("action" + str(action_id), lang)}"""
                                     , reply_markup= markup)





#reduct_btn
@router.callback_query(IsAdminFilter(), 
                       kboard_admin.AdminCallbackFactory.filter(F.action == "reduct_btn"))
async def reduct_btn_handler(callback: types.CallbackQuery, 
                             callback_data: kboard_admin.AdminCallbackFactory, state: FSMContext): 
    user_id = callback.from_user.id
    lang = db.get_lang(user_id)
    action_id = callback_data.value
    await callback.message.delete()
    await callback.message.answer(f"Старое название:{get_button_name('action' + str(action_id), lang)}. Введите новое название кнопки. Пожалуйста учитывайте, что её размеры должны быть ограничены, возможен перенос строки с использованием \\n.")
    await state.update_data(action_id=action_id)
    await state.set_state(StatesReductBtn.reduct_btn)


@router.message(StatesReductBtn.reduct_btn)
async def reduct_btn_text_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    user_data = await state.get_data()
    action_id = user_data["action_id"]
    btn_name = message.text
    db.update_button_name(action_id, btn_name, lang)
    text.menus = db.get_menus_text()
    kboard_admin.menu_dict = kboard_admin.getMenues()
    kboard.menu_dict = kboard.getMenues()
    await state.clear()
    markup = kboard_admin.get_action_menus(action_id,lang)
    await message.answer(f"""Текст сообщения:{get_action_msg(action_id - 1, lang)} \n Текст кнопки: {get_button_name("action" + str(action_id), lang)}"""
                                     , reply_markup= markup)



#del
@router.callback_query(IsAdminFilter(), 
                       kboard_admin.AdminCallbackFactory.filter(F.action == "del_btn"))
async def del_btn_handler(callback: types.CallbackQuery, 
                             callback_data: kboard_admin.AdminCallbackFactory, state: FSMContext): 
    user_id = callback.from_user.id
    lang = db.get_lang(user_id)
    action_id = callback_data.value
    buttons_list = db.get_buttons_list_by_column("action" + str(action_id))
    parent_action_id = int(buttons_list[len(buttons_list) - 1][6 : ])
    db.del_button("action" + str(action_id))
    text.buttons_list = db.get_buttons_list()
    kboard_admin.menu_dict = kboard_admin.getMenues()
    kboard.menu_dict = kboard.getMenues()  
    markup = kboard_admin.get_action_menus(parent_action_id,lang)
    await callback.message.edit_text(f"""Текст сообщения:{get_action_msg(parent_action_id - 1, lang)} \n Текст кнопки: {get_button_name("action" + str(parent_action_id), lang)}"""
                                     , reply_markup= markup)



#add
@router.callback_query(IsAdminFilter(), 
                       kboard_admin.AdminCallbackFactory.filter(F.action == "add_btn"))
async def add_btn_handler(callback: types.CallbackQuery, 
                             callback_data: kboard_admin.AdminCallbackFactory, state: FSMContext): 
    await state.update_data(parent_id=callback_data.value)
    await callback.message.delete()
    await callback.message.answer(f"""Введите сообщение, которое будет вылазить при появлении кнопки.""", parse_mode=ParseMode.HTML)
    await state.set_state(StateAddBtn.add_msg)

@router.message(StateAddBtn.add_msg)
async def new_msg_btn_handler(message: types.Message, state: FSMContext):
    await message.answer(f"""Введите название кнопки.""", parse_mode=ParseMode.HTML)
    await state.update_data(msg=message.text)
    await state.set_state(StateAddBtn.add_btn)

@router.message(StateAddBtn.add_btn)
async def new_name_btn_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)  
    btn_data = await state.get_data()
    btn_id = db.add_new_action_describtion([btn_data["msg"], message.text], lang=lang)
    if(btn_id):
        db.add_buttons_list(btn_id, "action" + str(btn_data["parent_id"]))

    parent_action_id = btn_data["parent_id"]

    await state.clear()

    text.buttons_list = db.get_buttons_list()
    text.menus = db.get_menus_text()
    kboard_admin.menu_dict = kboard_admin.getMenues()
    kboard.menu_dict = kboard.getMenues() 

    markup = kboard_admin.get_action_menus(parent_action_id,lang)
    await message.answer(f"""Текст сообщения:{get_action_msg(parent_action_id - 1, lang)} \n Текст кнопки: {get_button_name("action" + str(parent_action_id), lang)}"""
                                     , reply_markup= markup)


@router.callback_query(IsAdminFilter(), 
                    kboard_admin.AdminCallbackFactory.filter(F.action == "action"))
async def reduct_action_handler(callback: types.CallbackQuery, 
                             callback_data: kboard_admin.AdminCallbackFactory):
    user_id = callback.from_user.id
    lang = db.get_lang(user_id)  
    action_id = callback_data.value
    markup = kboard_admin.get_action_menus(action_id,lang)
    await callback.message.edit_text(f"""Текст сообщения:{get_action_msg(action_id - 1, lang)} \n Текст кнопки: {get_button_name("action" + str(action_id), lang)}"""
                                     , reply_markup= markup)


#редактирование формы
@router.callback_query(IsAdminFilter(), 
                    kboard_admin.AdminCallbackFactory.filter(F.action == "reduct_form"))
async def start_reduct_form_handler(callback: types.CallbackQuery):

    markup = kboard_admin.reduct_form_markup
    await callback.message.edit_text("""В данной форме можно редактировать только текст, который появляется при заполнении формы пользователем.""", reply_markup= markup, parse_mode=ParseMode.HTML)


@router.callback_query(IsAdminFilter(), 
                    kboard_admin.AdminCallbackFactory.filter(F.action == "reduct_form_text"))
async def reduct_form_text_handler(callback: types.CallbackQuery, 
                             callback_data: kboard_admin.AdminCallbackFactory, state: FSMContext):
    markup = get_reply_markup("cancel", "ru")
    await callback.message.delete()
    await callback.message.answer("Введите новый текст.", reply_markup=markup, parse_mode=ParseMode.HTML)
    await state.update_data(key=callback_data.value)
    await state.set_state(StatesReductForm.writing_new_text)

@router.callback_query(IsAdminFilter(), 
                    kboard_admin.AdminCallbackFactory.filter(F.action == "text"))
async def select_form_text_handler(callback: types.CallbackQuery, 
                             callback_data: kboard_admin.AdminCallbackFactory):
    user_id = callback.from_user.id
    lang = db.get_lang(user_id) 
    num = callback_data.value
    markup = get_markup_reduct_forms_text(num)
    await callback.message.edit_text(f"""Вопрос: {get_text("text" + str(num), lang=lang)}\nОтвет, в случае неверного ответа: {get_text("text" + str(num + 1), lang=lang)}""",
    reply_markup= markup, parse_mode=ParseMode.HTML)


@router.message(StatesReductForm.writing_new_text, F.text.lower() == "отмена")
async def cancel_reduct_form(message: types.Message, state: FSMContext):
    await state.clear()


    await message.answer("""Отмена прошла успешно.""", reply_markup =types.ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)

    markup = kboard_admin.reduct_form_markup
    await message.answer("""В данной форме можно редактировать только текст, который появляется при заполнении формы пользователем.""", reply_markup= markup, parse_mode=ParseMode.HTML)
  



@router.message(StatesReductForm.writing_new_text)
async def save_reduct_form_text_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id) 
    data = await state.get_data()
    if(db.update_text_table("text" + str(data["key"]), message.text, lang)):
        text.text = db.get_text()
        await message.answer("""Изменения прошли успешно.""", reply_markup =types.ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)
    await state.clear()

    markup = kboard_admin.reduct_form_markup
    await message.answer("""В данной форме можно редактировать только текст, который появляется при заполнении формы пользователем.""", reply_markup= markup, parse_mode=ParseMode.HTML)
  

def get_markup_reduct_forms_text(num: int):
    texts = ["Изменить вопрос","Изменить ответ", "Назад"]
    actions = ["reduct_form_text", "reduct_form_text", "reduct_form"]

    values = [num, num + 1,0]
    values.append(0)
    return kboard_admin.create_inline_keyboard_builder(texts, actions, values)