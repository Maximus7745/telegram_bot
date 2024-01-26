from aiogram import types, Router, F
from kboard import NumbersCallbackFactory
from aiogram.filters import StateFilter
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
import kboard
from text import get_action_msg, get_text, db
router = Router()



@router.callback_query(StateFilter(None), NumbersCallbackFactory.filter(F.action == "action" and F.value == 67))
async def list_forms_handler(callback: types.CallbackQuery, 
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


@router.callback_query(
     StateFilter(None), NumbersCallbackFactory.filter(F.action == "check_form")
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
     StateFilter(None), NumbersCallbackFactory.filter(F.action == "reduct_form")
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
     StateFilter(None), NumbersCallbackFactory.filter(F.action == "send_red_form")
)
async def send_reduct_form_hundler(callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory):
        db.update_elem_by_id("is_reviewed", False, callback_data.value)
        await check_form_hundler(callback, callback_data)