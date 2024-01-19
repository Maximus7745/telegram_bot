from db import Database
from config import host, user, password, database
db = Database(host, user, password, database)

text = db.get_text()
buttons_list = db.get_buttons_list()
menus = db.get_menus_text()

def get_button_name(action, lang):
    id = int(action[6 : ])
    num = 2
    match lang:
        case "ru":
                num = 4
        case "fr":
                num = 6
        case "ar":
                num = 8
        case "ch":
                num = 10
        case _:
                num = 2
    return menus[id - 1][num]

def get_action_msg(id, lang = "en"):
    num = 2
    match lang:
        case "ru":
                num = 3
        case "fr":
                num = 5
        case "ar":
                num = 7
        case "ch":
                num = 9
        case _:
                num = 1
    return menus[id][num]
       
def get_text(key, lang = "en"):
    match lang:
        case "ru":
                num = 1
        case "fr":
                num = 2
        case "ar":
                num = 3
        case "ch":
                num = 4
        case _:
                num = 0
    return text[key][num]

def get_text_for_all_lang(key: str)-> [str]:
       return [text[key][num].lower() for num in range(0,5)]


