from aiogram import types, F, Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
import kboard
from magic_filter import F
from kboard import NumbersCallbackFactory
from aiogram.filters import CommandStart
#from data.text import message_dict
from aiogram.filters import Command, StateFilter
from aiogram.enums import ParseMode
router = Router()
from aiogram.types import FSInputFile
import random
import file
from aiogram.fsm.context import FSMContext

#from data.text import action_dict, list_dict
# from bot import db, bot
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import kboard
from text import get_action_msg, get_text, get_text_for_all_lang, db
from states import StatesContuctSupport
from handlers import form
from hundlers_admin import admin, admin_bot_reduct, admin_forms, admin_questions, admin_spam,admin_statistic, admin_right

from handlers import form_reduct

@router.message(CommandStart())
async def start_handler(message: Message):
        user_id = message.from_user.id
        is_authorization = db.check_user(user_id)
        if(is_authorization):
                lang = db.get_lang(user_id)
                await message.answer(get_action_msg(0,lang), reply_markup= kboard.get_action_menus(1,lang), parse_mode=ParseMode.HTML)
        else:
                await message.answer("Select your language",reply_markup=kboard.lang_marup, parse_mode=ParseMode.HTML)

@router.callback_query(NumbersCallbackFactory.filter(F.value == 66))
async def select_lang_hundler(callback: types.CallbackQuery, 
        callback_data: NumbersCallbackFactory):
        await callback.message.edit_text("Select your language",reply_markup=kboard.lang_marup, parse_mode=ParseMode.HTML)

@router.callback_query(NumbersCallbackFactory.filter(F.action == "lang"))
async def lang_event_hundler(callback: types.CallbackQuery, 
        callback_data: NumbersCallbackFactory):
        lang = callback_data.string
        user_id = callback.from_user.id
        is_authorization = db.check_user(user_id)
        if(is_authorization): 
                db.update_lang(user_id, lang)
        else:
                db.add_user(user_id, callback.from_user.username, lang)
        await callback.message.edit_text(get_action_msg(0,lang), 
                                     reply_markup= kboard.get_action_menus(1,lang), 
                                     parse_mode=ParseMode.HTML)
        

@router.callback_query(NumbersCallbackFactory.filter(F.value == 15))
async def useful_tips_hundler(callback: types.CallbackQuery, 
        callback_data: NumbersCallbackFactory):
        user_id = callback.from_user.id
        lang = db.get_lang(user_id)
        num = random.randint(1,6)
        await callback.message.edit_text(get_text("advice" + str(num), lang= lang), 
                                     reply_markup= kboard.get_action_menus(callback_data.value, lang), 
                                     parse_mode=ParseMode.HTML)
        

@router.callback_query(NumbersCallbackFactory.filter(F.value == 12))
async def first_step_hundler(callback: types.CallbackQuery, 
        callback_data: NumbersCallbackFactory):
        user_id = callback.from_user.id
        lang = db.get_lang(user_id)
        await callback.message.delete()
        if(lang == "ru"):
                await callback.message.answer_photo(file.get_file("photo1705054721"), allow_sending_without_reply=True)
                await callback.message.answer_photo(file.get_file("photo1705054721_1"), allow_sending_without_reply=True)
        else:
                await callback.message.answer_photo(file.get_file("first_steps_page1"), allow_sending_without_reply=True)
                await callback.message.answer_photo(file.get_file("first_steps_page2"), allow_sending_without_reply=True)
        await callback.message.answer(get_action_msg(callback_data.value - 1, lang), 
                                        reply_markup= kboard.get_action_menus(callback_data.value,lang), 
                                        parse_mode=ParseMode.HTML)
        

@router.callback_query(NumbersCallbackFactory.filter(F.value == 8))
async def visa_form_hundler(callback: types.CallbackQuery, 
        callback_data: NumbersCallbackFactory):
        user_id = callback.from_user.id
        lang = db.get_lang(user_id)
        await callback.message.delete()
        await callback.message.answer_document(file.get_file("Visa_application_form_example"), allow_sending_without_reply=True)
        await callback.message.answer_document(file.get_file("Visa_application_form"), allow_sending_without_reply=True)
        await callback.message.answer(get_action_msg(callback_data.value - 1, lang), 
                                                reply_markup= kboard.get_action_menus(callback_data.value,lang), 
                                                parse_mode=ParseMode.HTML)
        
@router.callback_query(NumbersCallbackFactory.filter(F.value == 68))
async def writting_questions_hundler(callback: types.CallbackQuery, 
        callback_data: NumbersCallbackFactory, state: FSMContext):
        user_id = callback.from_user.id
        lang = db.get_lang(user_id)
        await callback.message.delete()
        await callback.message.answer(get_action_msg(callback_data.value - 1, lang), 
                                                reply_markup= kboard.get_reply_markup("cancel", lang), 
                                                parse_mode=ParseMode.HTML)
        await state.set_state(StatesContuctSupport.writting_questions)

@router.message(StatesContuctSupport.writting_questions, F.text.lower().in_(get_text_for_all_lang("text29")))
async def cancel_writting_questions_hundler(message: types.Message, state: FSMContext):
        await state.clear()
        action_id = 14
        user_id = message.from_user.id
        lang = db.get_lang(user_id)
        await message.answer(get_text("text74", lang=lang), reply_markup =types.ReplyKeyboardRemove())
        await message.answer(get_action_msg(action_id - 1, lang), 
                                                reply_markup= kboard.get_action_menus(action_id, lang), 
                                                parse_mode=ParseMode.HTML)
        await state.set_state(StatesContuctSupport.writting_questions)

@router.message(
    StatesContuctSupport.writting_questions, F.text
)
async def send_questions_hundler(message: Message, state: FSMContext):
        await state.clear()
        user_id = message.from_user.id
        lang = db.get_lang(user_id)
        db.add_new_question(user_id, message.text)
        await message.answer(get_text("text35",lang=lang),reply_markup = types.ReplyKeyboardRemove(), 
        parse_mode=ParseMode.HTML)
        action_id = 14
        await message.answer(get_action_msg(action_id - 1, lang), 
                                                reply_markup= kboard.get_action_menus(action_id, lang), 
                                                parse_mode=ParseMode.HTML)
        

@router.callback_query(NumbersCallbackFactory.filter(F.value == 67))
async def list_forms_hundler(callback: types.CallbackQuery, 
        callback_data: NumbersCallbackFactory, state: FSMContext):
        user_id = callback.from_user.id
        lang = db.get_lang(user_id)
        forms = db.get_forms_by_user_id(user_id)
        texts = [get_text("text39", lang) + " " + str(i) for i in range(1, min(len(forms) + 1, 6))]
        texts.append(get_text("text28", lang=lang))
        values = [int(forms[i]) for i in range(min(len(forms),5))]
        values.append(7)
        actions = ["check_form" for i in range(min(len(forms),5))]
        actions.append("action")
        markup = kboard.create_inline_keyboard_builder(texts, actions, values)
        await callback.message.edit_text(get_action_msg(callback_data.value - 1, lang), 
                                                reply_markup= markup, 
                                                parse_mode=ParseMode.HTML)
        await state.set_state(StatesContuctSupport.writting_questions)

@router.callback_query(
     NumbersCallbackFactory.filter(F.action == "check_form")
)
async def check_form_hundler(callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory):
        user_id = callback.from_user.id
        lang = db.get_lang(user_id)
        form_id = callback_data.value
        elems = db.get_all_elem_by_form_id(form_id)
        text = kboard.get_text_reduct_form_users(lang, elems)
        if(bool(elems[18]) and not bool(elems[19])):
                text = get_text("text40", lang=lang) + " " + get_text("text33", lang=lang) + db.get_form_comment(form_id) + "\n" \
                + text
                markup = kboard.create_inline_keyboard_builder([get_text("text56", lang=lang), get_text("text28", lang=lang)], 
                                                                          ["reduct_form", "action"], 
                                                                          [form_id, 67])
        elif(bool(elems[19])):
                text = get_text("text40", lang=lang) + " " + get_text("text42", lang=lang) + "\n" \
                + text 
                markup = kboard.create_inline_keyboard_builder([get_text("text28", lang=lang)], ["action"], [67])
        else:
                text = get_text("text40", lang=lang) + " " + get_text("text41", lang=lang) + "\n" \
                + text 
                markup = kboard.create_inline_keyboard_builder([get_text("text28", lang=lang)], ["action"], [67])
        

        await callback.message.edit_text(text, 
                                     reply_markup = markup, 
                                     parse_mode=ParseMode.HTML)
        
@router.callback_query(
     NumbersCallbackFactory.filter(F.action == "reduct_form")
)
async def reduct_form_hundler(callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory):
        user_id = callback.from_user.id
        lang = db.get_lang(user_id)
        form_id = callback_data.value
        elems = db.get_all_elem_by_form_id(form_id)
        text = get_text("text40", lang=lang) + " " + get_text("text33", lang=lang) + db.get_form_comment(form_id) + "\n" \
                + kboard.get_text_reduct_form_users(lang, elems) + get_text("text58", lang=lang)
        markup = kboard.get_markup_reduct_forms_users(lang, form_id)


        await callback.message.edit_text(text, 
                                     reply_markup= markup, 
                                     parse_mode=ParseMode.HTML)

@router.callback_query(
     NumbersCallbackFactory.filter(F.action == "send_red_form")
)
async def send_reduct_form_hundler(callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory):
        db.update_elem_by_id("is_reviewed", False, callback_data.value)
        await check_form_hundler(callback, callback_data)

#Добавить ограничение по количеству и возможность просматривать старые заявки
@router.callback_query(NumbersCallbackFactory.filter(F.value == 69))
async def list_questions_hundler(callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory):
        user_id = callback.from_user.id
        lang = db.get_lang(user_id)
        questions = db.get_questions_by_user_id(user_id)
        actions = ["check_questions"] * len(questions)
        actions.append("action")
        values = list(map(lambda x: int(x[1]), questions))
        values.append(14)
        texts = list(map(lambda x: str(x[0]), questions))
        texts.append(get_text("text28", lang=lang))
        markup = kboard.create_inline_keyboard_builder(texts, actions, values)
        await callback.message.edit_text(get_action_msg(callback_data.value - 1, lang), 
                                                reply_markup= markup, 
                                                parse_mode=ParseMode.HTML)

@router.callback_query(NumbersCallbackFactory.filter(F.action == "check_questions"))
async def list_forms_hundler(callback: types.CallbackQuery, 
        callback_data: NumbersCallbackFactory, state: FSMContext):
        user_id = callback.from_user.id
        lang = db.get_lang(user_id)
        answer = db.get_answer_by_id(callback_data.value)
        question = db.get_question_by_id(callback_data.value)
        if(answer is None):
                answer = get_text("text37", lang = lang)

        markup = kboard.create_inline_keyboard_builder([get_text("text28", lang=lang)], ["action"], [69])
        await callback.message.edit_text(str(question) + " \n " + str(answer), reply_markup = markup, 
        parse_mode=ParseMode.HTML)



@router.callback_query(NumbersCallbackFactory.filter(F.action == "action"))
async def menu_event_hundler(callback: types.CallbackQuery, 
        callback_data: NumbersCallbackFactory):
        user_id = callback.from_user.id
        lang = db.get_lang(user_id)
        await callback.message.edit_text(get_action_msg(callback_data.value - 1, lang), 
                                     reply_markup= kboard.get_action_menus(callback_data.value, lang), 
                                     parse_mode=ParseMode.HTML)



