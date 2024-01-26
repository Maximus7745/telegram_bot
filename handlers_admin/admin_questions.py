from filters import IsAdminFilter 
from aiogram import types, Router, F

from aiogram.enums import ParseMode
from states import StatesAnswerQuestions
from bot import bot
from aiogram.fsm.context import FSMContext


from aiogram.filters import Command, StateFilter
import kboard_admin
from text import db


from kboard import get_reply_markup

from text import get_text
from translate import get_tranlate

router = Router()


@router.callback_query(IsAdminFilter(), 
                       kboard_admin.AdminCallbackFactory.filter(F.action == "questions"))
async def select_question_handler(callback: types.CallbackQuery):
    questions = db.get_new_questions()
    markup = get_markup_questions(questions)

    await callback.message.edit_text(f"""За время вашего отсутствия поступило {len(questions)} вопросов. Выберите вопрос для ответа на него.""",
    reply_markup=markup, parse_mode=ParseMode.HTML)



@router.callback_query(IsAdminFilter(), 
                       kboard_admin.AdminCallbackFactory.filter(F.action == "check_question"))
async def check_question_handler(callback: types.CallbackQuery, 
                             callback_data: kboard_admin.AdminCallbackFactory, state: FSMContext): 
    if(not db.check_question_by_id(callback_data.value)):
        db.update_question_by_id("is_open", True, callback_data.value)
        question_id = callback_data.value
        question = str(db.get_question_by_id(question_id))
        tranlate_text = get_tranlate(question)
        if(tranlate_text):
            text = "Перевод: " + tranlate_text + "\nВопрос: " + str(question) + "\nВведите ответ на вопрос"
        else:
            text = "Вопрос: " + str(question) + "\nВведите ответ на вопрос"
        await callback.message.delete()

        await callback.message.answer(text, 
                                    reply_markup = get_reply_markup("cancel", "ru"), 
                                    parse_mode=ParseMode.HTML)
        await state.set_state(StatesAnswerQuestions.writting_answer)
        await state.update_data(question_id=question_id)


@router.message(StatesAnswerQuestions.writting_answer, F.text.lower() == "отмена")
async def cancel_ask(message: types.Message, state: FSMContext):

    data = await state.get_data()
    question_id = data["question_id"]
    db.update_question_by_id("is_open", False, question_id)
    await state.clear()
    
    await message.answer("Ответ на вопрос не был записан", reply_markup =types.ReplyKeyboardRemove())
    questions = db.get_new_questions()
    markup = get_markup_questions(questions)

 
    await message.answer(f"""За время вашего отсутствия поступило {len(questions)} вопросов. Выберите вопрос для ответа на него.""",
    reply_markup=markup, parse_mode=ParseMode.HTML)


@router.message(StatesAnswerQuestions.writting_answer)
async def send_answer_handler(message: types.message, state: FSMContext):
    data = await state.get_data()
    question_id = data["question_id"]
    await state.clear()
    if(db.answer_question(question_id, message.text)):
        await message.answer("""Ответ был успешно записан.""", reply_markup =types.ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)
        db.update_question_by_id("is_open", False, question_id)
    user_id = db.get_user_by_id(question_id)
    lang = db.get_lang(user_id)
    await bot.send_message(user_id, get_text("text36", lang=lang))



    questions = db.get_new_questions()
    markup = get_markup_questions(questions)

 
    await message.answer(f"""За время вашего отсутствия поступило {len(questions)} вопросов. Выберите вопрос для ответа на него.""",
    reply_markup=markup, parse_mode=ParseMode.HTML)


def get_markup_questions(questions):
    texts = list()
    actions = list()
    values = list()
    for i in range(min(4, len(questions))):   
        texts.append(questions[i][1])
        actions.append("check_question")
        values.append(int(questions[i][0]))
    texts.append("Назад")
    actions.append("start")
    values.append(0)
    return kboard_admin.create_inline_keyboard_builder(texts, actions, values)