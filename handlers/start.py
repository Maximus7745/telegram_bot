from aiogram import types, Router, F
from kboard import NumbersCallbackFactory
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
import random
import kboard
import file
from text import get_action_msg, get_text, db
import text
router = Router()
from states import StatesFAQ
from bot import bot
from classification import find_closest_answer

@router.message(CommandStart())
async def start_handler(message: types.Message):
        user_id = message.from_user.id
        is_authorization = db.check_user(user_id)
        if(is_authorization):
                lang = db.get_lang(user_id)
                await message.answer(get_action_msg(0,lang), reply_markup= kboard.get_action_menus(1,lang), parse_mode=ParseMode.HTML)
        else:
                await message.answer("Select your language",reply_markup=kboard.lang_marup, parse_mode=ParseMode.HTML)

@router.callback_query(StateFilter(None), NumbersCallbackFactory.filter(F.action == "action" and F.value == 66))
async def select_lang_handler(callback: types.CallbackQuery):
        await callback.message.edit_text("Select your language",reply_markup=kboard.lang_marup, parse_mode=ParseMode.HTML)

@router.callback_query(StateFilter(None), NumbersCallbackFactory.filter(F.action == "lang"))
async def lang_event_handler(callback: types.CallbackQuery, 
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
        

@router.callback_query(StateFilter(None), NumbersCallbackFactory.filter(F.action == "action" and F.value == 15))
async def useful_tips_handler(callback: types.CallbackQuery, 
        callback_data: NumbersCallbackFactory):
        user_id = callback.from_user.id
        lang = db.get_lang(user_id)
        num = random.randint(1,6)
        await callback.message.edit_text(get_text("advice" + str(num), lang= lang), 
                                     reply_markup= kboard.get_action_menus(callback_data.value, lang), 
                                     parse_mode=ParseMode.HTML)
        

@router.callback_query(StateFilter(None), NumbersCallbackFactory.filter(F.action == "action" and F.value == 12))
async def first_step_handler(callback: types.CallbackQuery, 
        callback_data: NumbersCallbackFactory):
        user_id = callback.from_user.id
        lang = db.get_lang(user_id)
        await callback.message.delete()
        if(lang == "ru"):
                files = file.get_files("first_steps_ru")
                for f in files:
                        await callback.message.answer_photo(f, allow_sending_without_reply=True)
        else:
                files = file.get_files("first_steps_en")
                for f in files:
                        await callback.message.answer_photo(f, allow_sending_without_reply=True)
        await callback.message.answer(get_action_msg(callback_data.value - 1, lang), 
                                        reply_markup= kboard.get_action_menus(callback_data.value,lang), 
                                        parse_mode=ParseMode.HTML)
        

@router.callback_query(StateFilter(None), NumbersCallbackFactory.filter(F.action == "action" and F.value == 8))
async def visa_form_handler(callback: types.CallbackQuery, 
        callback_data: NumbersCallbackFactory):
        user_id = callback.from_user.id
        lang = db.get_lang(user_id)
        files = file.get_files("visa_application_form")
        await callback.message.delete()
        for f in files:
                await callback.message.answer_document(f, allow_sending_without_reply=True)
        await callback.message.answer(get_action_msg(callback_data.value - 1, lang), 
                                                reply_markup= kboard.get_action_menus(callback_data.value,lang), 
                                                parse_mode=ParseMode.HTML)
        

@router.callback_query(StateFilter(None), 
                       NumbersCallbackFactory.filter(F.action == "action" and F.value.in_(list(map(lambda x: int(x[6 : ]),text.buttons_list["action6"][ : -1])))))
async def menu_event_handler(callback: types.CallbackQuery, 
        callback_data: NumbersCallbackFactory, state: FSMContext):
        user_id = callback.from_user.id
        lang = db.get_lang(user_id)
        await state.set_state(StatesFAQ.select_question)
        await callback.message.delete()
        await callback.message.answer(get_action_msg(callback_data.value - 1, lang), 
                                     reply_markup= kboard.markups[callback_data.value][lang], 
                                     parse_mode=ParseMode.HTML)


@router.message(
    StatesFAQ.select_question, F.text.in_(text.get_text_for_all_lang("text29"))
)
async def cancel_answer_faq(message: types.Message, state: FSMContext):
        user_id = message.from_user.id
        lang = db.get_lang(user_id)
        await state.clear()
        msg = await message.answer(get_action_msg(5, lang), 
                                        reply_markup= types.ReplyKeyboardRemove(), 
                                        parse_mode=ParseMode.HTML)
        await bot.delete_message(user_id, message_id=msg.message_id)
        await message.answer(get_action_msg(5, lang), reply_markup= kboard.get_action_menus(6, lang), 
                                        parse_mode=ParseMode.HTML)
@router.message(
    StatesFAQ.select_question
)
async def answer_faq_handler(message: types.Message, state: FSMContext):

        user_id = message.from_user.id
        lang = db.get_lang(user_id)
        action_id = text.get_action_name(message.text, lang)
        await state.clear()
        msg = await message.answer(get_action_msg(action_id - 1, lang), 
                                        reply_markup= types.ReplyKeyboardRemove(), 
                                        parse_mode=ParseMode.HTML)
        await bot.delete_message(user_id, message_id=msg.message_id)
        await message.answer(get_action_msg(action_id - 1, lang), 
                                        reply_markup= kboard.get_action_menus(action_id, lang), 
                                        parse_mode=ParseMode.HTML)




@router.callback_query(StateFilter(None), NumbersCallbackFactory.filter(F.action == "action"))
async def menu_event_handler(callback: types.CallbackQuery, 
        callback_data: NumbersCallbackFactory, state: FSMContext):
        user_id = callback.from_user.id
        lang = db.get_lang(user_id)
        await callback.message.edit_text(get_action_msg(callback_data.value - 1, lang), 
                                     reply_markup= kboard.get_action_menus(callback_data.value, lang), 
                                     parse_mode=ParseMode.HTML)
        



@router.message(StateFilter(None), F.text)
async def get_answer(message: types.Message):
        await message.answer(find_closest_answer(message.text))