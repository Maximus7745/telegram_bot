from handlers.start import router
from filters import IsAdminFilter 
from aiogram import types
from magic_filter import F
from aiogram.enums import ParseMode
from states import StatesReductBtn, StatesReductMsg, StateAddBtn, StatesAdmin, StatesReductForm, StatesCancelForm, StatesReductApplication, StatesAnswerQuestions
from aiogram.types import FSInputFile
from bot import bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from aiogram.filters import Command, StateFilter
import kboard_admin
from text import db, get_text, get_action_msg, get_button_name
import text

from kboard import get_reply_markup
import kboard







@router.callback_query(IsAdminFilter(), 
                       kboard_admin.AdminCallbackFactory.filter(F.action == "reduct"))
async def start_reduct_bot_hundler(callback: types.CallbackQuery):
    markup = kboard_admin.start_reduct_bot_markup
    await callback.message.edit_text("""Раздел редактирования бота делится на два подраздела. Редактирование меню включает в себя редактировние стартового меню, которое видят пользователи при взаимодействии с ботом, а также изменение и добавление частозадаваемых вопросов. Редактировние формы же предполагает непосредственно изменение текста при заполнении пользователями формы для обучения.""", 
    reply_markup= markup, parse_mode=ParseMode.HTML)

@router.callback_query(IsAdminFilter(), 
                       kboard_admin.AdminCallbackFactory.filter(F.action == "select_lang"))
async def check_list_lang_reduct_hundler(callback: types.CallbackQuery):
    await callback.message.edit_text("Select your language", 
                                     reply_markup= kboard_admin.lang_marup, parse_mode=ParseMode.HTML)

@router.callback_query(IsAdminFilter(), 
                       kboard_admin.AdminCallbackFactory.filter(F.action == "lang"))
async def select_lang_reduct_hundler(callback: types.CallbackQuery, 
                             callback_data: kboard_admin.AdminCallbackFactory):
    lang = callback_data.string
    user_id = callback.from_user.id
    db.update_lang(user_id, lang)
    await start_reduct_bot_hundler(callback)
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
    await start_reduct_bot_hundler(callback=callback)



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
@router.callback_query(IsAdminFilter(), F.data.contains("reduct_btn_action"))
async def handle_reduct_btn(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    lang = db.get_lang(user_id)  
    action = callback.data.split("_")[3]
    await callback.message.edit_text(f"Старое название:{db.get_button_name(action[6:], lang)}. Введите новое название кнопки. Пожалуйста учитывайте, что её размеры должны быть ограничены, возможен перенос строки с использованием \\n.", reply_markup=None)
    await state.update_data(action=callback.data)
    await state.set_state(StatesReductBtn.reduct_btn)

@router.message(StatesReductBtn.reduct_btn)
async def handle_reduct_text(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)  
    user_data = await state.get_data()
    action = user_data["action"].split("_")[3]
    id = action[6:]
    btn_name = message.text
    db.update_button_name(id, btn_name, lang)
    
    await send_reducted_menu(action, message)
    await state.clear()




#del
@router.callback_query(IsAdminFilter(), F.data.contains("del_btn_action"))
async def handle_del_btn(callback: types.CallbackQuery):
    action = callback.data.split("_")[3]
    buttons_list = db.get_buttons_list(action)
    parent_action = buttons_list[len(buttons_list) - 1]
    db.del_button(action)
    await send_reducted_menu(parent_action, callback.message)



#add
@router.callback_query(IsAdminFilter(), F.data.contains("add_btn_action"))
async def handle_add_btn(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(parent_id=str(callback.message.reply_markup.inline_keyboard[0][0].callback_data.split("action")[1]))
    await callback.message.delete()
    await callback.message.answer(f"""Введите сообщение, которое будет вылазить при появлении кнопки.""", parse_mode=ParseMode.HTML)
    await state.set_state(StateAddBtn.add_msg)

@router.message(StateAddBtn.add_msg)
async def handle_add_btn(message: types.Message, state: FSMContext):
    await message.answer(f"""Введите название кнопки.""", parse_mode=ParseMode.HTML)
    await state.update_data(msg=message.text)
    await state.set_state(StateAddBtn.add_btn)

@router.message(StateAddBtn.add_btn)
async def handle_add_btn(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)  
    btn_data = await state.get_data()
    btn_id = db.add_new_action_describtion([btn_data["msg"], message.text], lang=lang)
    db.add_buttons_list(btn_id, [], "action" + btn_data["parent_id"])

    await state.clear()
    texts = ["Редактирование бота", "Обработка заявок", "Просмотр статистики", "Добавление новых администраторов и блокировка пользователей", "Сделать рассылку"]
    actions = ["8dei_reduct", "8dei_processing_applications", "8dei_statistics", "8dei_rights_distribution", "8dei_add_spam"]
    markup = kboard.create_inline_keyboard_builder_for_admins(texts, actions) 
    await message.answer("""Добро пожаловать! Выберите интересующий вас 
    раздел и приступайте к администрированию телеграм бота.""", reply_markup= markup, parse_mode=ParseMode.HTML)    
# надо доделать!!!!!
# @router.callback_query(IsAdminFilter(), F.data == "action15")
# async def handle_reduct(callback: types.CallbackQuery):
#     user_id = callback.from_user.id
#     lang = db.get_lang(user_id)  
#     action = "action15"
#     id = 15
#     list_advices = db.get_advices_list()
#     texts = ["Редактировать текст", "Редактировать кнопку", "Удалить кнопку", "Добавить\nновый совет"]
#     buttons_list = db.get_buttons_list(action)
#     for btn in buttons_list:
#         if(btn != buttons_list[len(buttons_list) - 1]):
#             texts.append(db.get_button_name(btn[6 : ], lang))
#     texts.append("Назад")
#     actions = [f"8dei_reduct_msg_{action}", f"8dei_reduct_btn_{action}",f"8dei_del_btn_{action}", f"8dei_add_btn_{action}"]
#     actions += buttons_list
#     markup = kboard.create_inline_keyboard_builder_for_admins(texts, actions) 
#     await callback.message.edit_text(f"""Текст сообщения:{db.get_message(id, lang)} \n Текст кнопки: {db.get_button_name(id, lang)}""", reply_markup= markup, parse_mode=ParseMode.HTML)


#тут ещё нужно добавить обработки особых случаев, по типу полезных советов и добавления нивых советов
#main functions for actions
#Потом оптимизировать со следующим
@router.callback_query(IsAdminFilter(), 
                    kboard_admin.AdminCallbackFactory.filter(F.action == "action"))
async def reduct_action_hundler(callback: types.CallbackQuery, 
                             callback_data: kboard_admin.AdminCallbackFactory):
    user_id = callback.from_user.id
    lang = db.get_lang(user_id)  
    action_id = callback_data.value
    markup = kboard_admin.get_action_menus(action_id,lang)
    await callback.message.edit_text(f"""Текст сообщения:{get_action_msg(action_id - 1, lang)} \n Текст кнопки: {get_button_name("action" + str(action_id), lang)}"""
                                     , reply_markup= markup)


#плюс не забыть добавить отмену при вводе текста
#да и для формы тоже

#редактирование формы
@router.callback_query(IsAdminFilter(), 
                    kboard_admin.AdminCallbackFactory.filter(F.action == "reduct_form"))
async def start_reduct_form_hundler(callback: types.CallbackQuery):

    markup = kboard_admin.reduct_form_markup
    await callback.message.edit_text("""В данной форме можно редактировать только текст, который появляется при заполнении формы пользователем.""", reply_markup= markup, parse_mode=ParseMode.HTML)


@router.callback_query(IsAdminFilter(), 
                    kboard_admin.AdminCallbackFactory.filter(F.action == "reduct_form_text"))
async def reduct_form_text_hundler(callback: types.CallbackQuery, 
                             callback_data: kboard_admin.AdminCallbackFactory, state: FSMContext):
    markup = get_reply_markup("cancel", "ru")
    await callback.message.delete()
    await callback.message.answer("Введите новый текст.", reply_markup=markup, parse_mode=ParseMode.HTML)
    await state.update_data(key=callback_data.value)
    await state.set_state(StatesReductForm.writing_new_text)

@router.callback_query(IsAdminFilter(), 
                    kboard_admin.AdminCallbackFactory.filter(F.action == "text"))
async def select_form_text_hundler(callback: types.CallbackQuery, 
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
async def save_reduct_form_text_hundler(message: types.Message, state: FSMContext):
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