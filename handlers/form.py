from states import StatesForm
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import types, F, Router
from aiogram.types import Message
from kboard import NumbersCallbackFactory
from validate_email import validate_email
import kboard
from aiogram.enums import ParseMode
import re
import filters
import file
from text import get_text, get_text_for_all_lang, get_action_msg, db
router = Router()

@router.callback_query(StateFilter(None),NumbersCallbackFactory.filter(F.action == "action" and F.value == 58))
async def start_form(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    lang = db.get_lang(user_id)
    await callback.message.delete()
    await callback.message.answer(text= get_text("text1", lang=lang), 
    reply_markup=kboard.get_reply_markup("cancel", lang))
    await state.set_state(StatesForm.writing_firstname)

#можно потом разобраться с дропом голосовых и файлов в неподходящий момент или просто в try except обернуть, либо в фильтрах текст прописать
@router.message(StatesForm.writing_firstname, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesForm.writing_lastname, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesForm.writing_country, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesForm.writing_birth_date, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesForm.writing_mail, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesForm.writing_phone, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesForm.writing_old_counties_educations, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesForm.loading_passport, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesForm.loading_passport_translation, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesForm.loading_photo, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesForm.loading_visa_form, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesForm.loading_bank_statement, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesForm.select_person_access, F.text.lower().in_(get_text_for_all_lang("text29")))
@router.message(StatesForm.loading_comments, F.text.lower().in_(get_text_for_all_lang("text29")))
async def cancel_form(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(get_text("text32", lang=lang), reply_markup =types.ReplyKeyboardRemove())
    await message.answer(get_action_msg(1, lang), reply_markup = kboard.get_action_menus(1, lang), parse_mode=ParseMode.HTML)

#writing_firstname

@router.message(
    StatesForm.writing_firstname,  F.text,
    lambda m: re.fullmatch(r'^[a-zA-Zа-яА-Я\s\-\'.]+$', m.text) and len(m.text) < 50 
)
async def firstname_written(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await state.update_data(firstname=message.text)
    await message.answer(
        text=get_text("text3", lang=lang)
    )

    
    await state.set_state(StatesForm.writing_lastname)

@router.message(StatesForm.writing_firstname)
async def firstname_written_incorrectly(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(
        text=get_text("text2", lang=lang)
    )






#writing_lastname
@router.message(
    StatesForm.writing_lastname,  F.text,
    lambda m: re.fullmatch(r'^[a-zA-Zа-яА-Я\s\-\'.]+$', m.text) and len(m.text) < 50 
)
async def lastname_written(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await state.update_data(lastname=message.text)
    await message.answer(
        text=get_text("text5", lang=lang), 
        reply_markup=kboard.get_reply_markup("countries", lang)
    )
    await state.set_state(StatesForm.writing_country)

@router.message(StatesForm.writing_lastname)
async def firstname_written_incorrectly(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(
        text=get_text("text4", lang=lang)
    )





#writing_country
@router.message(
    StatesForm.writing_country,  F.text,
    lambda m: re.fullmatch(r'^[a-zA-Zа-яА-Я\s\-\'.]+$', m.text) and len(m.text) < 50 
)
async def country_written(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await state.update_data(country=message.text)
    await message.answer(
        text=get_text("text7", lang=lang), reply_markup=kboard.get_reply_markup("cancel", lang)
    )
    await state.set_state(StatesForm.writing_birth_date)

@router.message(StatesForm.writing_country)
async def country_written_incorrectly(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(
        text=get_text("text6", lang=lang)
    )





#можно добавить проперку, чтобы дата была старше сегодняшней
#подумать как можно улучшить проверку даты
#writing_birth_date
@router.message(
    StatesForm.writing_birth_date,  F.text,
    lambda m: re.fullmatch("[0-3][0-9]\.[0-1][0-9]\.[1-2][0-9][0-9][0-9]",m.text)
    #datetime.strptime(date_string, "%d.%m.%Y")
)
async def birth_date_written(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await state.update_data(birth_date=message.text)
    await message.answer(
        text=get_text("text9", lang=lang)
    )
    await state.set_state(StatesForm.writing_mail)

@router.message(StatesForm.writing_birth_date)
async def birth_date_written_incorrectly(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(
        text=get_text("text8", lang=lang)
    )






#writing_mail
@router.message(
    StatesForm.writing_mail,  F.text,
    lambda m: validate_email(email_address=m.text)
)
async def mail_written(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await state.update_data(mail=message.text)
    await message.answer(
        text=get_text("text11", lang=lang)
    )
    await state.set_state(StatesForm.writing_phone)

@router.message(StatesForm.writing_mail)
async def mail_written_incorrectly(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(
        text=get_text("text10", lang=lang)
    )






#writing_phone
@router.message(
    StatesForm.writing_phone, F.text,
    lambda m: ((m.text[0] == "+" and len(m.text) > 1) or m.text[0].isdigit()) and all(x.isdigit() for x in m.text[1 : ]) and len(m.text) < 33
)
async def phone_written(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await state.update_data(phone=message.text)
    await message.answer(
        text=get_text("text13", lang=lang), 
        reply_markup=kboard.get_reply_markup("countries", lang)
    )
    await state.set_state(StatesForm.writing_old_counties_educations)

@router.message(StatesForm.writing_phone)
async def phone_written_incorrectly(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(
        text=get_text("text12", lang=lang)
    )






#writing_old_counties_educations
@router.message(
    StatesForm.writing_old_counties_educations, F.text,
    lambda m: re.fullmatch(r'^[a-zA-Zа-яА-Я\s\-\'.]+$', m.text) and len(m.text) < 50 
)
async def old_counties_educations_written(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await state.update_data(before_study_country=message.text)
    await message.answer(
        text=get_text("text15", lang=lang), reply_markup=kboard.get_reply_markup("cancel", lang)
    )
    await state.set_state(StatesForm.loading_passport)

@router.message(StatesForm.writing_old_counties_educations)
async def old_counties_educations_written_incorrectly(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(
        text=get_text("text14", lang=lang)
    )




 
#loading_passport 
@router.message(
    StatesForm.loading_passport,
    F.document,
    filters.IsPdfOrJpg()
)
async def passport_written(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    file_id = message.document.file_id
    file_info = await message.bot.get_file(file_id)
    file_path = file_info.file_path
    await message.bot.download_file(file_path=file_path, destination= "users_docs/passports/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1])
    await state.update_data(passport="users_docs/passports/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1])
    await message.answer(
        text=get_text("text17", lang=lang)
    )
    await state.set_state(StatesForm.loading_passport_translation)


@router.message(
    StatesForm.loading_passport,
    F.photo[-1].as_("photo"),
    filters.IsJpg()
)
async def passport_written_by_photo(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    file_id = message.photo[-1].file_id 
    file_info = await message.bot.get_file(file_id)
    file_path = file_info.file_path
    await message.bot.download_file(file_path=file_path, destination= "users_docs/passports/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1])
    await state.update_data(passport="users_docs/passports/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1])
    await message.answer(
        text=get_text("text17", lang=lang)
    )
    await state.set_state(StatesForm.loading_passport_translation)


@router.message(StatesForm.loading_passport)
async def passport_written_incorrectly(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(
        text=get_text("text16", lang=lang))




#loading_passport_translation
@router.message(
    StatesForm.loading_passport_translation, 
    F.document,
    filters.IsPdfOrJpg()
)
async def passport_translation_written(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    file_id = message.document.file_id
    file_info = await message.bot.get_file(file_id)
    file_path = file_info.file_path
    await message.bot.download_file(file_path=file_path, destination= "users_docs/passport_tranlate/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1])
    await state.update_data(passport_tranlation="users_docs/passport_tranlate/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1])
    await message.answer(
        text=get_text("text76", lang=lang)
    )
    await state.set_state(StatesForm.loading_photo)


@router.message(
    StatesForm.loading_passport_translation, 
    F.photo[-1].as_("photo"),
    filters.IsJpg()
)
async def passport_translation_written_by_photo(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    # await message.photo[-1].download(destination_file='data/rgrg.jpg')
    #add_photo(message.from_user.id, photo.file_id, photo.file_unique_id)
    file_id = message.photo[-1].file_id 
    file_info = await message.bot.get_file(file_id)
    file_path = file_info.file_path
    await message.bot.download_file(file_path=file_path, destination= "users_docs/passport_tranlate/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1])
    await state.update_data(passport_tranlation="users_docs/passport_tranlate/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1])
    await message.answer(
        text=get_text("text76", lang=lang)
    )
    await state.set_state(StatesForm.loading_photo)


@router.message(StatesForm.loading_passport_translation)
async def passport_translation_written_incorrectly(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(
        text=get_text("text18", lang=lang)
    )


#photo
@router.message(
    StatesForm.loading_photo, 
    F.document,
    filters.IsJpeg()
)
async def load_photo(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    file_id = message.document.file_id
    file_info = await message.bot.get_file(file_id)
    file_path = file_info.file_path
    await message.bot.download_file(file_path=file_path, destination= "users_docs/photo/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1])
    await state.update_data(photo="users_docs/photo/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1])
    files = file.get_files("visa_application_form")
    for f in files:
        await message.answer_document(f, allow_sending_without_reply=True)
    await message.answer(
        text=get_text("text19", lang=lang)
    )
    await state.set_state(StatesForm.loading_visa_form)


@router.message(
    StatesForm.loading_photo, 
    F.photo[-1].as_("photo"),
    filters.IsJpg()
)
async def load_photo_by_photo(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    file_id = message.photo[-1].file_id 
    file_info = await message.bot.get_file(file_id)
    file_path = file_info.file_path
    await message.bot.download_file(file_path=file_path, destination= "users_docs/photo/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1])
    await state.update_data(photo="users_docs/photo/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1])
    files = file.get_files("visa_application_form")
    for f in files:
        await message.answer_document(f, allow_sending_without_reply=True)
    await message.answer(
        text=get_text("text19", lang=lang)
    )
    await state.set_state(StatesForm.loading_visa_form)


@router.message(StatesForm.loading_photo)
async def load_photo_incorrectly(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(
        text=get_text("text77", lang=lang)
    )


#loading_visa_form
@router.message(
    StatesForm.loading_visa_form,
    F.document,
    filters.IsPdfOrJpg()
)
async def visa_form_written(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    file_id = message.document.file_id
    file_info = await message.bot.get_file(file_id)
    file_path = file_info.file_path
    await message.bot.download_file(file_path=file_path, destination= "users_docs/visa/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1])
    await state.update_data(application_form="users_docs/visa/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1])
    await message.answer(
        text=get_text("text21", lang=lang)
    )
    await state.set_state(StatesForm.loading_bank_statement)


@router.message(
    StatesForm.loading_visa_form,
    F.photo[-1].as_("photo"),
    filters.IsJpg()
)
async def visa_form_written_by_photo(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    file_id = message.photo[-1].file_id 
    file_info = await message.bot.get_file(file_id)
    file_path = file_info.file_path
    await message.bot.download_file(file_path=file_path, destination= "users_docs/visa/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1])
    await state.update_data(application_form="users_docs/visa/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1])
    await message.answer(
        text=get_text("text21", lang=lang)
    )
    await state.set_state(StatesForm.loading_bank_statement)

@router.message(StatesForm.loading_visa_form)
async def visa_form_written_incorrectly(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(
        text=get_text("text20", lang=lang)
    )






#loading_bank_statement 
@router.message(
    StatesForm.loading_bank_statement,
    F.document,
    filters.IsPdfOrJpg()
)
async def bank_statement_written(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    file_id = message.document.file_id
    file_info = await message.bot.get_file(file_id)
    file_path = file_info.file_path
    await message.bot.download_file(file_path=file_path, destination= "users_docs/bank_statement/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1])
    await state.update_data(bank_statment="users_docs/bank_statement/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1])
    await message.answer(
        text=get_text("text23", lang=lang), 
        reply_markup=kboard.get_reply_markup("person_access", lang)
    )
    await state.set_state(StatesForm.select_person_access)


@router.message(
    StatesForm.loading_bank_statement,
    F.photo[-1].as_("photo"),
    filters.IsJpg()
)
async def bank_statement_written_by_photo(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    file_id = message.photo[-1].file_id 
    file_info = await message.bot.get_file(file_id)
    file_path = file_info.file_path
    await message.bot.download_file(file_path=file_path, destination= "users_docs/bank_statement/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1])
    await state.update_data(bank_statment="users_docs/bank_statement/" + str(file_id) + "." + file_path.split(".")[len(file_path.split(".")) - 1])
    await message.answer(
        text=get_text("text23", lang=lang), 
        reply_markup=kboard.get_reply_markup("person_access", lang)
    )
    await state.set_state(StatesForm.select_person_access)

@router.message(StatesForm.loading_bank_statement)
async def bank_statement_written_incorrectly(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(
        text=get_text("text22", lang=lang)
    )






#select_person_access
@router.message(
    StatesForm.select_person_access, F.text,
    lambda m: m.text.lower() in get_text_for_all_lang("text30") or m.text.lower() in get_text_for_all_lang("text31")
)
async def person_access_written(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    if(message.text.lower() in get_text_for_all_lang("text31")):
        await state.update_data(yourself_applying=False)
    else:
        await state.update_data(yourself_applying=True)
    await message.answer(
        text=get_text("text25", lang=lang), reply_markup=kboard.get_reply_markup("cancel", lang)
    )
    await state.set_state(StatesForm.loading_comments)

@router.message(StatesForm.select_person_access)
async def person_access_written_incorrectly(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(
        text=get_text("text24", lang=lang)
    )






#loading_comments
@router.message(
    StatesForm.loading_comments, F.text
)
async def comments_written(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(text=get_text("text27", lang=lang), reply_markup =types.ReplyKeyboardRemove())
    await message.answer(get_action_msg(2, lang), reply_markup= kboard.get_action_menus(2, lang), parse_mode=ParseMode.HTML)
    #send form
    user_data = await state.get_data()
    await state.clear()
    user_data["comments"] = message.text
    user_data["is_full"] = True 
    db.add_new_form(user_id,user_data)



@router.message(StatesForm.loading_comments)
async def comments_written_incorrectly(message: Message):
    user_id = message.from_user.id
    lang = db.get_lang(user_id)
    await message.answer(
        text=get_text("text26", lang=lang)
    )










