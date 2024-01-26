from states import StatesReductOldForm
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import F
from kboard import NumbersCallbackFactory
from aiogram.types import Message
from aiogram import types, Router
from validate_email import validate_email
import kboard
from aiogram.enums import ParseMode
import re
from aiogram.types import FSInputFile
import filters
from datetime import datetime
from kboard import NumbersCallbackFactory
from text import get_action_msg, get_text, get_text_for_all_lang, db
router = Router()


@router.callback_query(NumbersCallbackFactory.filter(F.action == "red_form_elem"))
async def start_red_form_elem_form(callback: types.CallbackQuery, 
        callback_data: NumbersCallbackFactory, state: FSMContext):
    user_id = callback.from_user.id
    lang = db.get_lang(user_id)
    form_id = callback_data.value
    param = callback_data.string
    await callback.message.delete()
    match param:
        case "firstname":
            await state.set_state(StatesReductOldForm.writing_firstname)
            text = get_text("text59" ,lang=lang) + db.get_elem_by_id("firstname", form_id)
        case "lastname":
            await state.set_state(StatesReductOldForm.writing_lastname)
            text = get_text("text60" ,lang=lang) + db.get_elem_by_id("lastname", form_id)
        case "country":
            await state.set_state(StatesReductOldForm.writing_country)
            text = get_text("text61" ,lang=lang) + db.get_elem_by_id("country", form_id)
        case "birth_date":
            await state.set_state(StatesReductOldForm.writing_birth_date)
            text = get_text("text62" ,lang=lang) + db.get_elem_by_id("birth_date", form_id)
        case "mail":
            await state.set_state(StatesReductOldForm.writing_mail)
            text = get_text("text63" ,lang=lang) + db.get_elem_by_id("mail", form_id)
        case "phone":
            await state.set_state(StatesReductOldForm.writing_phone)
            text = get_text("text64" ,lang=lang) + db.get_elem_by_id("phone", form_id)
        case "before_study_country":
            await state.set_state(StatesReductOldForm.writing_old_counties_educations)
            text = get_text("text65" ,lang=lang) + db.get_elem_by_id("before_study_country", form_id)

        case "comments":
            await state.set_state(StatesReductOldForm.loading_comments)
            text = get_text("text66" ,lang=lang) + db.get_elem_by_id("comments", form_id)
        #Здесь стоит удалять прошлые файлы, наверное
        case "passport":
            await state.set_state(StatesReductOldForm.loading_passport)
            text = get_text("text67" ,lang=lang)
            await callback.message.answer_document(FSInputFile(db.get_elem_by_id("passport", form_id)), allow_sending_without_reply=True)
        case "passport_tranlation":
            await state.set_state(StatesReductOldForm.loading_passport_translation)
            text = get_text("text68" ,lang=lang)
            await callback.message.answer_document(FSInputFile(db.get_elem_by_id("passport_tranlation", form_id)), allow_sending_without_reply=True)
        case "application_form":
            await state.set_state(StatesReductOldForm.loading_visa_form)
            text = get_text("text69" ,lang=lang)
            await callback.message.answer_document(FSInputFile(db.get_elem_by_id("application_form", form_id)), allow_sending_without_reply=True)
        case "bank_statment":
            await state.set_state(StatesReductOldForm.loading_bank_statement)
            text = get_text("text70" ,lang=lang)
            await callback.message.answer_document(FSInputFile(db.get_elem_by_id("bank_statment", form_id)), allow_sending_without_reply=True)
        case _:
            await state.set_state(StatesReductOldForm.loading_photo)
            text = get_text("text71" ,lang=lang)
    await state.update_data(form_id=form_id)
    await callback.message.answer(text=text, 
    reply_markup=kboard.get_reply_markup("cancel", lang))
    

@router.message(StatesReductOldForm.writing_firstname, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesReductOldForm.writing_lastname, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesReductOldForm.writing_country, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesReductOldForm.writing_birth_date, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesReductOldForm.writing_mail, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesReductOldForm.writing_phone, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesReductOldForm.writing_old_counties_educations, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesReductOldForm.loading_passport, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesReductOldForm.loading_passport_translation, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesReductOldForm.loading_photo, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesReductOldForm.loading_visa_form, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesReductOldForm.loading_bank_statement, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesReductOldForm.select_person_access, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesReductOldForm.loading_comments, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesReductOldForm.loading_photo, F.text.lower().in_(get_text_for_all_lang("text29")))
async def cancel_reduct_form(message: Message, state: FSMContext):
    data = await state.get_data()
    form_id = data["form_id"]
    await state.clear()
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(get_text("text73", lang=lang), reply_markup =types.ReplyKeyboardRemove())

    elems = db.get_all_elem_by_form_id(form_id)
    text = get_text("text40", lang=lang) + " " + get_text("text33", lang=lang) + db.get_form_comment(form_id) + "\n" \
        + kboard.get_text_reduct_form_users(lang, elems) + get_text("text58", lang=lang)
    markup = kboard.get_markup_reduct_forms_users(lang, form_id)

    await message.answer(text, reply_markup = markup, 
    parse_mode=ParseMode.HTML)




#writing_firstname
@router.message(
    StatesReductOldForm.writing_firstname,  F.text,
    lambda m: re.fullmatch(r'^[a-zA-Zа-яА-Я\s\-\'.]+$', m.text) and len(m.text) < 50  
)
async def reduct_firstname_written(message: Message, state: FSMContext):
    data = await state.get_data()
    form_id = data["form_id"]
    db.update_elem_by_id("firstname", str(message.text), form_id)
    await load_start_red_menu(message, state=state)


@router.message(StatesReductOldForm.writing_firstname)
async def reduct_firstname_written_incorrectly(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(
        text=get_text("text2", lang=lang)
    )

async def load_start_red_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(get_text("text72", lang=lang), reply_markup =types.ReplyKeyboardRemove())
    data = await state.get_data()
    form_id = data["form_id"]
    await state.clear()
    elems = db.get_all_elem_by_form_id(form_id)
    text = get_text("text40", lang=lang) + " " + get_text("text33", lang=lang) + db.get_form_comment(form_id) + "\n" \
        + kboard.get_text_reduct_form_users(lang, elems) + get_text("text58", lang=lang)
    markup = kboard.get_markup_reduct_forms_users(lang, form_id)

    await message.answer(text, reply_markup = markup, 
    parse_mode=ParseMode.HTML)




#writing_lastname
@router.message(
    StatesReductOldForm.writing_lastname,  F.text,
    lambda m: re.fullmatch(r'^[a-zA-Zа-яА-Я\s\-\'.]+$', m.text) and len(m.text) < 50 
)
async def reduct_lastname_written(message: Message, state: FSMContext):
    data = await state.get_data()
    form_id = data["form_id"]
    db.update_elem_by_id("lastname", str(message.text), form_id)
    await load_start_red_menu(message, state=state)

@router.message(StatesReductOldForm.writing_lastname)
async def reduct_firstname_written_incorrectly(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(
        text=get_text("text4", lang=lang)
    )





#writing_country
@router.message(
    StatesReductOldForm.writing_country,  F.text,
    lambda m: re.fullmatch(r'^[a-zA-Zа-яА-Я\s\-\'.]+$', m.text) and len(m.text) < 50 
)
async def reduct_country_written(message: Message, state: FSMContext):
    data = await state.get_data()
    form_id = data["form_id"]
    db.update_elem_by_id("country", str(message.text), form_id)
    await load_start_red_menu(message, state=state)

@router.message(StatesReductOldForm.writing_country)
async def reduct_country_written_incorrectly(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(
        text=get_text("text6", lang=lang)
    )





#можно добавить проперку, чтобы дата была старше сегодняшней
#подумать как можно улучшить проверку даты
#writing_birth_date
@router.message(
    StatesReductOldForm.writing_birth_date,  F.text,
    lambda m: re.fullmatch("[0-3][0-9]\.[0-1][0-9]\.[1-2][0-9][0-9][0-9]",m.text)
    #datetime.strptime(date_string, "%d.%m.%Y")
)
async def reduct_birth_date_written(message: Message, state: FSMContext):
    birth_date = datetime.datetime.strptime(message.text, "%d.%m.%Y").date()
    data = await state.get_data()
    form_id = data["form_id"]
    db.update_elem_by_id("birth_date", birth_date, form_id)
    await load_start_red_menu(message, state=state)

@router.message(StatesReductOldForm.writing_birth_date)
async def reduct_birth_date_written_incorrectly(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(
        text=get_text("text8", lang=lang)
    )






#writing_mail
@router.message(
    StatesReductOldForm.writing_mail,  F.text,
    lambda m: validate_email(email_address=m.text)
)
async def reduct_mail_written(message: Message, state: FSMContext):
    data = await state.get_data()
    form_id = data["form_id"]
    db.update_elem_by_id("mail", str(message.text), form_id)
    await load_start_red_menu(message, state=state)

@router.message(StatesReductOldForm.writing_mail)
async def reduct_mail_written_incorrectly(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(
        text=get_text("text10", lang=lang)
    )






#writing_phone
@router.message(
    StatesReductOldForm.writing_phone, F.text,
    lambda m: ((m.text[0] == "+" and len(m.text) > 1) or m.text[0].isdigit()) and all(x.isdigit() for x in m.text[1 : ]) and len(m.text) < 33 # maybe add check ( ) or space or -
)
async def reduct_phone_written(message: Message, state: FSMContext):
    data = await state.get_data()
    form_id = data["form_id"]
    db.update_elem_by_id("phone", str(message.text), form_id)
    await load_start_red_menu(message, state=state)

@router.message(StatesReductOldForm.writing_phone)
async def reduct_phone_written_incorrectly(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(
        text=get_text("text12", lang=lang)
    )






#writing_old_counties_educations
@router.message(
    StatesReductOldForm.writing_old_counties_educations, F.text,
    lambda m: re.fullmatch(r'^[a-zA-Zа-яА-Я\s\-\'.]+$', m.text) and len(m.text) < 50 
)
async def reduct_old_counties_educations_written(message: Message, state: FSMContext):
    data = await state.get_data()
    form_id = data["form_id"]
    db.update_elem_by_id("before_study_country", str(message.text), form_id)
    await load_start_red_menu(message, state=state)

@router.message(StatesReductOldForm.writing_old_counties_educations)
async def reduct_old_counties_educations_written_incorrectly(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(
        text=get_text("text14", lang=lang)
    )




#Добавить загрузку по фото а не только документом
 
#loading_passport 
@router.message(
    StatesReductOldForm.loading_passport,
    F.document,
    filters.IsPdfOrJpg()
)
async def reduct_passport_written(message: Message, state: FSMContext):
    data = await state.get_data()
    form_id = data["form_id"]
    file_id = message.document.file_id
    file_info = await message.bot.get_file(file_id)
    file_path = file_info.file_path
    await message.bot.download_file(file_path=file_path, 
    destination= "users_docs/passports/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1])
    db.update_elem_by_id("passport", "users_docs/passports/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1], form_id)
    await load_start_red_menu(message, state=state)


@router.message(StatesReductOldForm.loading_passport)
async def reduct_passport_written_incorrectly(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(
        text=get_text("text16", lang=lang))





#from storage import add_photo
#loading_passport_translation
@router.message(
    StatesReductOldForm.loading_passport_translation, 
    F.document,
    filters.IsPdfOrJpg()
)
async def reduct_passport_translation_written(message: Message, state: FSMContext):
    data = await state.get_data()
    form_id = data["form_id"]
    file_id = message.document.file_id
    file_info = await message.bot.get_file(file_id)
    file_path = file_info.file_path
    await message.bot.download_file(file_path=file_path, destination= "users_docs/passport_tranlate/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1])
    db.update_elem_by_id("passport", "users_docs/passport_tranlate/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1], form_id)
    await load_start_red_menu(message, state=state)


@router.message(StatesReductOldForm.loading_passport_translation)
async def reduct_passport_translation_written_incorrectly(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(
        text=get_text("text18", lang=lang)
    )






#loading_visa_form
@router.message(
    StatesReductOldForm.loading_visa_form,
    F.document,
    filters.IsPdfOrJpg()
)
async def reduct_visa_form_written(message: Message, state: FSMContext):
    data = await state.get_data()
    form_id = data["form_id"]
    file_id = message.document.file_id
    file_info = await message.bot.get_file(file_id)
    file_path = file_info.file_path
    await message.bot.download_file(file_path=file_path, destination= "users_docs/visa/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1])
    db.update_elem_by_id("passport", "users_docs/visa/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1], form_id)
    await load_start_red_menu(message, state=state)


@router.message(StatesReductOldForm.loading_visa_form)
async def reduct_visa_form_written_incorrectly(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(
        text=get_text("text20", lang=lang)
    )






#loading_bank_statement 
@router.message(
    StatesReductOldForm.loading_bank_statement,
    F.document,
    filters.IsPdfOrJpg()
)
async def reduct_bank_statement_written(message: Message, state: FSMContext):

    data = await state.get_data()
    form_id = data["form_id"]
    file_id = message.document.file_id
    file_info = await message.bot.get_file(file_id)
    file_path = file_info.file_path
    await message.bot.download_file(file_path=file_path, destination= "users_docs/bank_statement/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1])
    db.update_elem_by_id("passport", "users_docs/bank_statement/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1], form_id)
    await load_start_red_menu(message, state=state)


@router.message(StatesReductOldForm.loading_bank_statement)
async def reduct_bank_statement_written_incorrectly(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(
        text=get_text("text22", lang=lang)
    )






#select_person_access
# @router.message(
#     StatesReductOldForm.select_person_access, 
#     lambda m: m.text in db.get_text_for_all_lang("text30") or m.text in db.get_text_for_all_lang("text31")
# )
# async def reduct_person_access_written(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     lang = db.get_lang(user_id)
#     await state.update_data(person_access=message.text.lower())
#     await message.answer(
#         text=db.get_text("text25", lang=lang), reply_markup=kboard.createReplyKeyboardBuilder([db.get_text("text29", lang=lang)])
#     )
#     await state.set_state(StatesForm.loading_comments)

# @router.message(StatesReductOldForm.select_person_access)
# async def reduct_person_access_written_incorrectly(message: Message):
#     user_id = message.from_user.id
#     lang = db.get_lang(user_id)
#     await message.answer(
#         text=db.get_text("text24", lang=lang)
#     )






#loading_comments
@router.message(
    StatesReductOldForm.loading_comments, F.text
)
async def reduct_comments_written(message: Message, state: FSMContext):
    data = await state.get_data()
    form_id = data["form_id"]
    db.update_elem_by_id("comments", str(message.text), form_id)
    await load_start_red_menu(message, state=state)


@router.message(StatesReductOldForm.loading_comments)
async def reduct_comments_written_incorrectly(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(
        text=get_text("text26", lang=lang)
    )










