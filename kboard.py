import text
from aiogram.filters.callback_data import CallbackData
from typing import Optional

from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

def createReplyKeyboardBuilder(lines : [str]) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for line in lines:
        builder.add(KeyboardButton(text=line))
    return builder.as_markup()



class NumbersCallbackFactory(CallbackData, prefix="users"):
    action: str
    value: Optional[int] = None
    string: Optional[str] = None




def createInlineKeyboardBuilder( actions : [str], lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for action in actions:
        if(action == "action66" or action != actions[len(actions) - 1]):
            builder.button(text = text.get_button_name(action, lang), callback_data=NumbersCallbackFactory(action="action", 
                                                                                                       value= int(action[6 : ])))
        else:
            builder.button(text = text.get_text("text28", lang), callback_data=NumbersCallbackFactory(action="action", 
                                                                                                       value= int(action[6 : ])))
    builder.adjust(1)
    return builder.as_markup()



def getMenues():
    lang = ["en", "ru", "fr", "ar", "ch"]
    menu_dict = dict()
    for action in text.buttons_list:
        menu_dict[int(action[6 : ])] = dict()
        for l in lang:
            menu_dict[int(action[6 : ])][l] = createInlineKeyboardBuilder(text.buttons_list[action], l)
    return menu_dict

def load_markups():
    langs = ["en", "ru", "fr", "ar", "ch"]
    menu_dict = {
        "cancel" : dict(),
        "countries": dict(),
        "person_access": dict()
    }
    for lang in langs:
        menu_dict["cancel"][lang] = createReplyKeyboardBuilder([text.get_text("text29", lang)])
        menu_dict["countries"][lang] = createReplyKeyboardBuilder([text.get_text("country1", lang=lang), text.get_text("country2", lang=lang),
        text.get_text("country3", lang=lang), text.get_text("country4", lang=lang), text.get_text("text29", lang=lang)])
        menu_dict["person_access"][lang] = createReplyKeyboardBuilder([text.get_text("text30", lang=lang), text.get_text("text31", lang=lang),
        text.get_text("text29", lang=lang)])
    return menu_dict


def getInlineKeyboardBuilder(name):
    return menu_dict[name]

def get_action_menus(id: int, lang: str)-> InlineKeyboardMarkup:
    return menu_dict[id][lang]

def get_reply_markup(key: str, lang: str)-> ReplyKeyboardMarkup:
    return reply_markups[key][lang]

reply_markups = load_markups()
menu_dict = getMenues()

builder = InlineKeyboardBuilder()
builder.button(text="Русский", callback_data=NumbersCallbackFactory(action="lang",string="ru"))
builder.button(text="English", callback_data=NumbersCallbackFactory(action="lang",string="en"))
builder.button(text="Français", callback_data=NumbersCallbackFactory(action="lang",string="fr"))
builder.button(text="عرب", callback_data=NumbersCallbackFactory(action="lang",string="ar"))
builder.button(text="中國人", callback_data=NumbersCallbackFactory(action="lang",string="ch"))


lang_marup = builder.as_markup()

def create_inline_keyboard_builder(texts, actions, values, strs = []) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if len(strs) == 0:
        for i in range(len(texts)):
            builder.button(text=texts[i], callback_data=NumbersCallbackFactory(action=actions[i], value= values[i]))
    else:
        for i in range(len(texts)):
            builder.button(text=texts[i], callback_data=NumbersCallbackFactory(action=actions[i], value= values[i], 
                                                                               string=strs[i]))      
    builder.adjust(1)
    return builder.as_markup()


def get_text_reduct_form_users(lang, elems):
    return text.get_text("text43", lang=lang) + ": " + str(elems[2]) + "\n" \
                + text.get_text("text44", lang=lang) + ": " + str(elems[3]) + "\n" \
                + text.get_text("text45", lang=lang) + ": " + str(elems[4]) + "\n" \
                + text.get_text("text46", lang=lang) + ": " + str(elems[5]) + "\n" \
                + text.get_text("text47", lang=lang) + ": " + str(elems[6]) + "\n" \
                + text.get_text("text48", lang=lang) + ": " + str(elems[7]) + "\n" \
                + text.get_text("text49", lang=lang) + ": " + str(elems[8]) + "\n" \
                + text.get_text("text50", lang=lang) + ": " + str(elems[15]) + "\n"

def get_markup_reduct_forms_users(lang, form_id):
    texts = [text.get_text("text43", lang=lang),
                text.get_text("text44", lang=lang), text.get_text("text45", lang=lang),
                text.get_text("text46", lang=lang), text.get_text("text47", lang=lang),
                text.get_text("text48", lang=lang), text.get_text("text49", lang=lang),
                text.get_text("text50", lang=lang), text.get_text("text51", lang=lang),
                text.get_text("text52", lang=lang), text.get_text("text53", lang=lang),
                text.get_text("text54", lang=lang), text.get_text("text55", lang=lang), 
                text.get_text("text57", lang=lang), text.get_text("text28", lang=lang)]
    actions = ["red_form_elem", "red_form_elem", "red_form_elem",
                "red_form_elem", "red_form_elem", "red_form_elem",
                "red_form_elem", "red_form_elem", "red_form_elem",
                "red_form_elem", "red_form_elem", "red_form_elem",
                "red_form_elem", "send_red_form", "check_form"]
    values = [form_id for i in range(15)]
    strs = ["firstname", "lastname","country",
                 "birth_date", "mail","phone",
                 "before_study_country", "comments","passport",
                 "passport_tranlation", "application_form","bank_statment",
                 "photo", "",""]
    return create_inline_keyboard_builder(texts, actions, values, strs)


# from typing import Optional
# from aiogram.filters.callback_data import CallbackData

# from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
# from aiogram.filters import Command
# #from data.text import action_dict, list_dict

# from bot import db
# from aiogram.enums import ParseMode
# class NumbersCallbackFactory(CallbackData, prefix="d332da"):
#     action: str
#     value: Optional[int] = None

# def createInlineKeyboardBuilder(action, lang) -> InlineKeyboardMarkup:
#     builder = InlineKeyboardBuilder()
#     lines = db.get_buttons_list(action)
#     for line in lines:
#         if(action == "action1" or line != lines[len(lines) - 1]):
#             id = line[6 : ]
#             builder.button(text=db.get_button_name(id, lang), callback_data=line, parse_mode=ParseMode.HTML)
#         else:
#             builder.button(text=db.get_text("text28", lang=lang), callback_data=line)
#     builder.adjust(1)

    
#     return builder.as_markup()




# # def createInlineKeyboardBuilder( lines : [str], act: str=None) -> InlineKeyboardMarkup:
# #     builder = InlineKeyboardBuilder()
# #     idx = 0
# #     for line in lines:
# #         builder.button(text=line, callback_data=NumbersCallbackFactory(action=action_dict[line]))
# #         idx += 1
# #     builder.adjust(1)
# #     return builder.as_markup()



# cancel_kboard =  createReplyKeyboardBuilder(["Отмена"])

# # def setMenues():
# #     for item in list_dict:
# #         menu_dict[item] = createInlineKeyboardBuilder(list_dict[item])

# # def getInlineKeyboardBuilder(name):
# #     return menu_dict[name]

# # setMenues()
