from aiogram import types, Router, F
from kboard import NumbersCallbackFactory
from aiogram.filters import StateFilter
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
import kboard
from text import get_action_msg, get_text, get_text_for_all_lang, db
from states import StatesContuctSupport


router = Router()



@router.callback_query(StateFilter(None), NumbersCallbackFactory.filter(F.action == "action" and F.value == 68))
async def writting_questions_handler(callback: types.CallbackQuery, 
        callback_data: NumbersCallbackFactory, state: FSMContext):
        user_id = callback.from_user.id
        lang = db.get_lang(user_id)
        await callback.message.delete()
        await callback.message.answer(get_action_msg(callback_data.value - 1, lang), 
                                                reply_markup= kboard.get_reply_markup("cancel", lang), 
                                                parse_mode=ParseMode.HTML)
        await state.set_state(StatesContuctSupport.writting_questions)

@router.message(StatesContuctSupport.writting_questions, F.text.lower().in_(get_text_for_all_lang("text29")))
async def cancel_writting_questions_handler(message: types.Message, state: FSMContext):
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
async def send_questions_handler(message: types.Message, state: FSMContext):
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
        
@router.message(
    StatesContuctSupport.writting_questions
)
async def validate_questions_handler(message: types.Message, state: FSMContext):
        user_id = message.from_user.id
        lang = db.get_lang(user_id)
        await message.answer(get_text("text75",lang=lang),reply_markup = types.ReplyKeyboardRemove(), 
        parse_mode=ParseMode.HTML)



@router.callback_query(StateFilter(None), NumbersCallbackFactory.filter(F.action == "action" and F.value == 69))
async def list_questions_handler(callback: types.CallbackQuery,
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

@router.callback_query(StateFilter(None), NumbersCallbackFactory.filter(F.action == "check_questions"))
async def list_forms_handler(callback: types.CallbackQuery, 
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