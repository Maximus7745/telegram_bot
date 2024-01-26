from filters import IsAdminFilter 
from aiogram import types, Router, F
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from bot import bot
from aiogram.fsm.context import FSMContext
from states import StatesCancelForm, StatesReductApplication
from aiogram.filters import Command, StateFilter
import kboard_admin
from text import db


from kboard import get_reply_markup

from text import get_text

router = Router()











@router.callback_query(IsAdminFilter(), 
                       kboard_admin.AdminCallbackFactory.filter(F.action == "forms"))
async def check_forms_list_handler(callback: types.CallbackQuery, 
                             callback_data: kboard_admin.AdminCallbackFactory):
    if(callback_data.value != 0):
        db.update_elem_by_id("is_open", False, callback_data.value)
    forms = db.get_new_forms()
    markup = get_markup_forms(forms)

 
    await callback.message.edit_text(f"""За время вашего отсутствия поступило {len(forms)} заявок. Выберите заяку для перехода к её рассмотрению.""",
    reply_markup=markup, parse_mode=ParseMode.HTML)


@router.callback_query(IsAdminFilter(), 
                       kboard_admin.AdminCallbackFactory.filter(F.action == "check_form"))
async def check_form_handler(callback: types.CallbackQuery, 
                             callback_data: kboard_admin.AdminCallbackFactory): 
    if(not bool(db.get_elem_by_id("is_open",callback_data.value))):
        form_id = callback_data.value
        elems = db.get_all_elem_by_form_id(form_id)
        db.update_elem_by_id("is_open", True, callback_data.value)
        await callback.message.delete()
        try:
            await callback.message.answer_document(FSInputFile(elems[9]), allow_sending_without_reply=True)
            await callback.message.answer_document(FSInputFile(elems[10]), allow_sending_without_reply=True)
            await callback.message.answer_document(FSInputFile(elems[11]), allow_sending_without_reply=True)
            await callback.message.answer_document(FSInputFile(elems[12]), allow_sending_without_reply=True)
            await callback.message.answer_document(FSInputFile(elems[13]), allow_sending_without_reply=True)
        except Exception as e:
            print(e)
        finally:


            markup = get_markup_reduct_forms(form_id)
            text = get_text_reduct_form(elems)

            await callback.message.answer(text,
            reply_markup=markup, parse_mode=ParseMode.HTML)

@router.callback_query(IsAdminFilter(), 
                       kboard_admin.AdminCallbackFactory.filter(F.action == "reduct_mistakes"))
async def reduct_mistakes_handler(callback: types.CallbackQuery, 
                             callback_data: kboard_admin.AdminCallbackFactory, state: FSMContext): 
    await state.set_state(StatesReductApplication.writing_text)
    await state.update_data(column=callback_data.string)
    await state.update_data(form_id=callback_data.value)
    await callback.message.delete()
    markup = get_reply_markup("cancel", "ru")
    await callback.message.answer("""Введите исправленные данные""", reply_markup=markup, parse_mode=ParseMode.HTML)    


@router.message(StatesReductApplication.writing_text, F.text.lower() == "отмена")
@router.message(StatesCancelForm.writing_casuse, F.text.lower() == "отмена")
async def cancel_reduct_mistakes(message: types.Message, state: FSMContext):
    data = await state.get_data()
    form_id = data["form_id"]

    await state.clear()


    await message.answer("""Отмена прошла успешно""", reply_markup =types.ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)
    
    elems = db.get_all_elem_by_form_id(form_id)
    try:
        await message.answer_document(FSInputFile(elems[9]), allow_sending_without_reply=True)
        await message.answer_document(FSInputFile(elems[10]), allow_sending_without_reply=True)
        await message.answer_document(FSInputFile(elems[11]), allow_sending_without_reply=True)
        await message.answer_document(FSInputFile(elems[12]), allow_sending_without_reply=True)
        await message.answer_document(FSInputFile(elems[13]), allow_sending_without_reply=True)
    except:
        pass
    finally:
        markup = get_markup_reduct_forms(form_id)
        text = get_text_reduct_form(elems)
 
        await message.answer(text,
        reply_markup=markup, parse_mode=ParseMode.HTML)


@router.message(StatesReductApplication.writing_text)
async def reduct_elem_handler(message: types.message, state: FSMContext):
    data = await state.get_data()
    column = data["column"]
    form_id = data["form_id"]
    if(db.update_elem_by_id(column, message.text, form_id)):
        await state.clear()
        await message.answer("""Данные успешно изменены""", reply_markup=types.ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)
    else:
        await message.answer("""Не удалось сохранить изменения""", reply_markup=types.ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)
    await state.clear()
    elems = db.get_all_elem_by_form_id(form_id)
    try:
        await message.answer_document(FSInputFile(elems[9]), allow_sending_without_reply=True)
        await message.answer_document(FSInputFile(elems[10]), allow_sending_without_reply=True)
        await message.answer_document(FSInputFile(elems[11]), allow_sending_without_reply=True)
        await message.answer_document(FSInputFile(elems[12]), allow_sending_without_reply=True)
        await message.answer_document(FSInputFile(elems[13]), allow_sending_without_reply=True)
    except:
        pass
    finally:

        
        markup = get_markup_reduct_forms(form_id)
        text = get_text_reduct_form(elems)

        await message.answer(text,
        reply_markup=markup, parse_mode=ParseMode.HTML)




@router.callback_query(IsAdminFilter(), 
                       kboard_admin.AdminCallbackFactory.filter(F.action == "return_form"))
async def return_form_handler(callback: types.CallbackQuery, 
                             callback_data: kboard_admin.AdminCallbackFactory, state: FSMContext):
    await state.set_state(StatesCancelForm.writing_casuse)
    await state.update_data(form_id=callback_data.value)
    await callback.message.delete()
    markup = get_reply_markup("cancel", "ru")
    await callback.message.answer("""Напишите причину отклонения формы.""", reply_markup=markup, parse_mode=ParseMode.HTML)    
    
@router.message(StatesCancelForm.writing_casuse)
async def write_casuse_handler(message: types.message, state: FSMContext):
    data = await state.get_data()
    form_id = data["form_id"]
    if(db.add_form_comment(form_id, str(message.text)) and db.update_elem_by_id("is_reviewed", True, form_id)):
        user_id = db.get_elem_by_id("user_id", form_id)
        user_lang = db.get_lang(user_id)
        await bot.send_message(user_id, get_text("text33", lang=user_lang) + message.text)
        await message.answer("""Форма успешно отклонена.""", reply_markup=types.ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)
    await state.clear()
    db.update_elem_by_id("is_open", False, form_id)

    forms = db.get_new_forms()
    markup = get_markup_forms(forms)

 
    await message.answer(f"""За время вашего отсутствия поступило {len(forms)} заявок. Выберите заяку для перехода к её рассмотрению.""",
    reply_markup=markup, parse_mode=ParseMode.HTML)




@router.callback_query(IsAdminFilter(), 
                       kboard_admin.AdminCallbackFactory.filter(F.action == "send_form"))
async def send_application(callback: types.CallbackQuery, 
                             callback_data: kboard_admin.AdminCallbackFactory): 
    form_id = callback_data.value
    db.update_elem_by_id("is_reviewed", True, form_id)
    db.update_elem_by_id("is_accepted", True, form_id)
    user_id = db.get_elem_by_id("user_id", form_id)
    user_lang = db.get_lang(user_id)
    db.update_elem_by_id("is_open", False, form_id)
    await bot.send_message(user_id, get_text("text34", lang=user_lang))
    #Тут должна быть ещё отправка в crm
    await check_forms_list_handler(callback, callback_data)




def get_markup_forms(forms):

    texts = list()
    actions = list()
    values = list()
    for i in range(1, min(5, len(forms) + 1)):   
        texts.append("Заявка № " + str(i))
        actions.append("check_form")
        values.append(int(forms[i - 1]))
    texts.append("Назад")
    actions.append("start")
    values.append(0)
    return kboard_admin.create_inline_keyboard_builder(texts, actions, values)



def get_markup_reduct_forms(form_id):

    texts = ["Принять", "Отказать", "Редактировать имя", 
        "Редактировать фамилию", "Редактировать страну", "Редактировать дату", "Редактировать почту", "Редактировать телефон",
        "Редактировать страну обучения", "Редактировать комментарий", "Назад"]
    actions = ["send_form", "return_form"]
    actions += ["reduct_mistakes"] * (len(texts) - 3) 
    actions.append("forms")
    strs = ["send_form", "return_form", "firstname", "lastname", "country", "birth_date",
               "mail", "phone", "before_study_country", "comments", "forms"]
    values = [form_id] * len(texts)
    return kboard_admin.create_inline_keyboard_builder(texts, actions, values, strs)


def get_text_reduct_form(elems):
    return "id: " + str(elems[1]) + "\nИмя: " + str(elems[2]) +  "\nФамилия: " + str(elems[3]) +  "\nСтрана: " +  \
    str(elems[4]) + "\nДата рождения: " + str(elems[5]) +  "\nПочта: " + str(elems[6]) +  \
    "\nТелефон: " + str(elems[7]) +  "\nСтрана обучения: " + str(elems[8]) +  "\nОтправил за себя: " + str(elems[14]) +  \
    "\nКомментарий: " + str(elems[15]) +  "\nДата подачи заявки" + str(elems[17])