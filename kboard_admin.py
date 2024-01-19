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



class AdminCallbackFactory(CallbackData, prefix="admin"):
    action: str
    value: Optional[int] = None
    string: Optional[str] = None




def createInlineKeyboardBuilder(num_action: int, actions : [str], lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text = "Редактировать текст", callback_data=AdminCallbackFactory(action="reduct_msg", value = num_action))
    builder.button(text = "Добавить новую кнопку", callback_data=AdminCallbackFactory(action="add_btn", value = num_action))
    if(num_action != 1):
        builder.button(text = "Редактировать кнопку", callback_data=AdminCallbackFactory(action="reduct_btn", value = num_action))
        builder.button(text = "Удалить кнопку", callback_data=AdminCallbackFactory(action="del_btn", value = num_action))
    for action in actions:
        if(action == "action66"):
            builder.button(text = "Назад", callback_data=AdminCallbackFactory(action="reduct", value = 0))
            continue

        if(action != actions[len(actions) - 1]):
            builder.button(text = text.get_button_name(action, lang), callback_data=AdminCallbackFactory(action="action", 
                                                                                                       value= int(action[6 : ])))
        else:
            builder.button(text = text.get_text("text28", lang), callback_data=AdminCallbackFactory(action="action", 
                                                                                                       value= int(action[6 : ])))
    builder.adjust(1)
    return builder.as_markup()



def getMenues():
    lang = ["en", "ru", "fr", "ar", "ch"]
    menu_dict = dict()
    for action in text.buttons_list:
        menu_dict[int(action[6 : ])] = dict()
        for l in lang:
            menu_dict[int(action[6 : ])][l] = createInlineKeyboardBuilder(int(action[6 : ]), text.buttons_list[action], l)
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
builder.button(text="Русский", callback_data=AdminCallbackFactory(action="lang",string="ru"))
builder.button(text="English", callback_data=AdminCallbackFactory(action="lang",string="en"))
builder.button(text="Français", callback_data=AdminCallbackFactory(action="lang",string="fr"))
builder.button(text="عرب", callback_data=AdminCallbackFactory(action="lang",string="ar"))
builder.button(text="中國人", callback_data=AdminCallbackFactory(action="lang",string="ch"))


lang_marup = builder.as_markup()


def create_inline_keyboard_builder(texts, actions, values, strs = []) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if len(strs) == 0:
        for i in range(len(texts)):
            builder.button(text=texts[i], callback_data=AdminCallbackFactory(action=actions[i], value= values[i]))
    else:
        for i in range(len(texts)):
            builder.button(text=texts[i], callback_data=AdminCallbackFactory(action=actions[i], value= values[i], 
                                                                               string=strs[i]))      
    builder.adjust(1)
    return builder.as_markup()

 
texts = ["Редактирование бота", "Обработка заявок", "Просмотр статистики", "Удаление администраторов", 
        "Сделать рассылку", "Ответить на вопросы"]
actions = ["reduct", "forms", "statistics", "rights_distribution", 
        "spam", "questions"]
values = [0] * len(texts)
start_markup = create_inline_keyboard_builder(texts, actions, values)

texts = ["Рассылка пользователям", "Рассылка администраторам", "Назад"]
actions = ["spam_users", "spam_admin", "start"]
values = [0] * len(texts)
spam_markup = create_inline_keyboard_builder(texts, actions, values) 

texts = ["Редактирование меню", "Редактирование формы", "Смена языка", "Вернуть изначальные данные", "Назад"]
actions = ["action", "reduct_form", "select_lang", "refrash_tables", "start"]
values = [1]
values += [0] * (len(texts) - 1)
start_reduct_bot_markup = create_inline_keyboard_builder(texts, actions, values)

texts = ["Имя","Фамилия","Страна","Дата рождения","Почта","Телефон","Страна обучения","Паспорт",
    "Перевод пасспорта","Виза","Выписка из банка","За кого заполняют","Комментарий", "Назад"]
actions = ["text"] * (len(texts) - 1)
actions.append("start")
values = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 0]
reduct_form_markup = create_inline_keyboard_builder(texts, actions, values)