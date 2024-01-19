import numpy as np
import pandas as pd
import mysql.connector
import datetime

class Database:
    def __init__(self, host, user, password, database):
        try:
            self.host = host
            self.user = user
            self.password = password
            self.database = database
            self.connection = None
            self.try_create_tables()
            self.try_load_start_data()

        except Exception as e:
            print(e)
            print("The connection has not been established")


    def connect(self)-> None:
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        

    def disconnect(self)-> None:
        if self.connection:
            self.connection.close()

    def try_create_tables(self)-> None:
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute("""CREATE TABLE IF NOT EXISTS 
                            menus(id INT AUTO_INCREMENT PRIMARY KEY, message TEXT, 
                            button_name VARCHAR(150), message_ru TEXT, button_name_ru VARCHAR(150), 
                            message_fr TEXT, button_name_fr VARCHAR(150), 
                            message_ar TEXT, button_name_ar VARCHAR(150), 
                            message_ch TEXT, button_name_ch VARCHAR(150));""")
                cursor.execute("""CREATE TABLE IF NOT EXISTS buttons_lists(id INT AUTO_INCREMENT PRIMARY KEY);""")
                cursor.execute("""CREATE TABLE IF NOT EXISTS text(id INT AUTO_INCREMENT PRIMARY KEY);""")
                cursor.execute("""CREATE TABLE IF NOT EXISTS users(id BIGINT PRIMARY KEY, 
                            language ENUM('ru', 'en', 'fr', 'ch', 'ar'), is_admin BOOL, username VARCHAR(32));""")
                cursor.execute("""CREATE TABLE IF NOT EXISTS forms(form_id INT AUTO_INCREMENT PRIMARY KEY, 
                            user_id BIGINT, firstname VARCHAR(50), lastname VARCHAR(50), country VARCHAR(50), 
                            birth_date DATE, mail VARCHAR(256), phone VARCHAR(32), before_study_country VARCHAR(50), 
                            passport VARCHAR(200), passport_tranlation VARCHAR(200), photo VARCHAR(200), 
                            application_form VARCHAR(200), bank_statment VARCHAR(200), yourself_applying BOOL, comments TEXT, admin_id BIGINT,
                            apply_date DATETIME, is_reviewed BOOL DEFAULT False, is_accepted BOOL DEFAULT False, 
                            FOREIGN KEY (user_id) REFERENCES users (id));""")
                cursor.execute("""CREATE TABLE IF NOT EXISTS forms_comment(id INT AUTO_INCREMENT PRIMARY KEY, form_id BIGINT,
                            admin_comment TEXT, comment_datetime DATETIME);""")
                cursor.execute("""CREATE TABLE IF NOT EXISTS telegram_questions(id INT AUTO_INCREMENT PRIMARY KEY, user_id BIGINT,
                            admin_id BIGINT, question TEXT, answer TEXT, question_datetime DATETIME, answer_datetime DATETIME);""")
                self.connection.commit()
        except Exception as e:
            print(e)
            print("Failed to create tables")
        finally:
            self.disconnect()

    def try_load_start_data(self)-> None:
        if(self.check_table_empety("buttons_lists")):
            self.set_start_data_buttons_list()
        if(self.check_table_empety("text")):
            self.set_start_data_text()
        if(self.check_table_empety("menus")):
            self.set_start_data_menus()

    def del_buttons_lists(self)-> bool:
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute("DROP TABLE buttons_lists;")
                return True
        except Exception as e:
            print(e)
            return False
        finally:
            self.disconnect()

    def create_buttons_lists(self)-> bool:
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute("CREATE TABLE buttons_lists(id INT AUTO_INCREMENT PRIMARY KEY);")
                return True
        except Exception as e:
            print(e)
            return False
        finally:
            self.disconnect()


    def del_text(self)-> bool:
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute("DROP TABLE text;")
                return True
        except Exception as e:
            print(e)
            return False
        finally:
            self.disconnect()

    def create_text(self)-> bool:
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute("CREATE TABLE text(id INT AUTO_INCREMENT PRIMARY KEY);")
                return True
        except Exception as e:
            print(e)
            return False
        finally:
            self.disconnect()

    def del_menus(self)-> bool:
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute("DROP TABLE menus;")
                return True
        except Exception as e:
            print(e)
            return False
        finally:
            self.disconnect()

    def create_menus(self)-> bool:
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute("""CREATE TABLE 
                            menus(id INT AUTO_INCREMENT PRIMARY KEY, message TEXT, 
                            button_name VARCHAR(150), message_ru TEXT, button_name_ru VARCHAR(150), 
                            message_fr TEXT, button_name_fr VARCHAR(150), 
                            message_ar TEXT, button_name_ar VARCHAR(150), 
                            message_ch TEXT, button_name_ch VARCHAR(150));""")
                return True
        except Exception as e:
            print(e)
            return False
        finally:
            self.disconnect()


    def check_table_empety(self, table_name: str)-> bool:
        try:
            result = [""]
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {table_name}")
                result = cursor.fetchall()
        except Exception as e:
            print(e)
            print(f"Failed load data to {table_name}")
        finally:
            self.disconnect()
            if len(result) == 0:
                    return True
            return False

    #forms_comment
#"""CREATE TABLE IF NOT EXISTS forms_comment(id INT AUTO_INCREMENT PRIMARY KEY, form_id BIGINT,
#                           admin_comment TEXT, comment_datetime DATETIME);"""
    def add_form_comment(self, form_id: int, admin_comment: str)-> bool:
        try:
            comment_datetime = datetime.datetime.now()
            self.connect()
            with self.connection.cursor() as cursor:
                query = "INSERT INTO forms_comment(form_id, admin_comment, comment_datetime) VALUES (%s, %s, %s);"
                params = (form_id, admin_comment, comment_datetime)
                cursor.execute(query,params)
                self.connection.commit()
                return True
        except Exception as e:
            print(e)
            return False
        finally:
            self.disconnect()

    def get_form_comment(self, form_id: int)-> str:
        try:
            self.connect()
            with self.connection.cursor(buffered=True) as cursor:
                query = "SELECT admin_comment FROM forms_comment WHERE form_id = %s;"
                params = (form_id, )
                cursor.execute(query,params)
                comment = cursor.fetchone()
                return comment[0]
        except Exception as e:
            print(e)
            return ""
        finally:
            self.disconnect()      
    #buttons_lists
    def set_start_data_buttons_list(self)-> None:
        try:
            data = pd.read_excel('data/excel_tables/buttons.xlsx').to_dict()
            for key in data.keys():
                column = dict()
                for row_num in data[key].keys():
                    elem = data[key][row_num]
                    if(pd.isnull(data[key][row_num])):
                        data[key] = column
                        break
                    else:
                        column[row_num] = data[key][row_num]
            self.connect()
            with self.connection.cursor() as cursor:
                for i in range(30):
                    cursor.execute(f"""INSERT INTO buttons_lists() VALUES();""")
                for key in data.keys():
                    cursor.execute(f"""ALTER TABLE buttons_lists ADD {key} VARCHAR(15) NULL;""")
                for key in data.keys():
                    for i in range(1, len(data[key]) + 1):
                        cursor.execute(f"""UPDATE buttons_lists SET {key} = %s WHERE id = %s;""", (data[key][i - 1], i))
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(e)
            print("Failed to load data into buttons_lists")
        finally:
            self.disconnect()


    def get_buttons_list(self)-> dict:
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'buttons_lists';")
                columns = cursor.fetchall()
                buttons_list = dict()
                for col in columns:
                    elem = col[0]
                    if elem != "id":
                        cursor.execute(f"""SELECT {elem} FROM buttons_lists;""")
                        actions = cursor.fetchall()
                        buttons_list[elem] = list(map(lambda x: x[0],list(filter(lambda x: x[0] is not None, actions))))
                return buttons_list
            
        except Exception as e:
            print(e)
            return dict()
        finally:
            self.disconnect()  


    def get_buttons_list_by_column(self, action: str)-> list[str]:
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute(f"""SELECT {action} FROM buttons_lists;""")
                actions = cursor.fetchall()
                return list(map(lambda x: x[0],list(filter(lambda x: x[0] is not None, actions))))

        except Exception as e:
            print(e)
            return list()
        finally:
            self.disconnect()  
            

    def add_buttons_list(self, id: int, parent_action: str)-> bool:

        try:
            parent_list = self.get_buttons_list_by_column(parent_action)
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute(f"""UPDATE buttons_lists SET {parent_action} = '{parent_list[len(parent_list) - 1]}' WHERE id = {len(parent_list) + 1};""")
                cursor.execute(f"""UPDATE buttons_lists SET {parent_action} = 'action{id}' WHERE id = {len(parent_list)};""")
                cursor.execute(f"""ALTER TABLE buttons_lists ADD action{id} VARCHAR(15) NULL;""")
                cursor.execute(f"""UPDATE buttons_lists SET action{id} = '{parent_action}' WHERE id = 1;""")
                self.connection.commit()  
                return True


        except Exception as e:
            self.connection.rollback()
            print(e)
            return False
        finally:
            self.disconnect()  

        
#по идеи тут ещё нужно удалять детей, но это необязательно
    def del_button(self, action: str)-> bool:
        try:
            buttons_list = self.get_buttons_list_by_column(action)
            parent_action = buttons_list[len(buttons_list) - 1]
            parent_butons_list = self.get_buttons_list_by_column(parent_action)
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute(f"""ALTER TABLE buttons_lists DROP COLUMN {action};""")
                shift_start = False
                for i in range(1, len(parent_butons_list)):
                    if(not shift_start):
                        if(parent_butons_list[i - 1] == action):
                            shift_start = True
                        else:
                            continue
                    cursor.execute(f"""UPDATE buttons_lists SET {parent_action} = %s WHERE id = {i};""", 
                                   (parent_butons_list[i],))

                cursor.execute(f"""UPDATE buttons_lists SET {parent_action} = NULL WHERE id = {len(parent_butons_list)};""")
            self.connection.commit()
            return True

        except Exception as e:
            self.connection.rollback()
            print(e)
            return False
        finally:
            self.disconnect()  
            


    #text
    def set_start_data_text(self)-> None:
        try:
            data = pd.read_excel('data/excel_tables/tranlate_text.xlsx').to_dict()
            for key in data.keys():
                column = dict()
                for row_num in data[key].keys():
                    elem = data[key][row_num]
                    if(pd.isnull(data[key][row_num])):
                        data[key] = column
                        break
                    else:
                        column[row_num] = data[key][row_num]
            self.connect()
            with self.connection.cursor() as cursor:
                for i in range(5):
                    cursor.execute("""INSERT INTO text() VALUES();""")
                for key in data.keys():
                    cursor.execute(f"""ALTER TABLE text ADD {key} TEXT NULL;""")
                for key in data.keys():
                    for i in range(1, len(data[key]) + 1):
                        cursor.execute(f"""UPDATE text SET {key} = %s WHERE id = %s;""", (data[key][i - 1], i))
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(e)
            print("Failed to load data into text")
        finally:
            self.disconnect()
    
    def get_text(self)-> dict:
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'text';")
                columns = cursor.fetchall()
            
        except Exception as e:
            print(e)
        finally:
            self.disconnect()  
        buttons_list = dict()
        for col in columns:
            key = col[0]
            if key != "id":
                text = self.get_text_for_all_lang(key)
                buttons_list[key] = list(map(lambda x: x[0],list(filter(lambda x: x[0] is not None, text))))
        return buttons_list


    # def get_text(self, key, lang = "en"):
    #     id = 1
    #     match lang:
    #         case "ru":
    #             id = 2
    #         case "fr":
    #             id = 3
    #         case "ar":
    #             id = 4
    #         case "ch":
    #             id = 5
    #         case _:
    #             id = 1

    #     with self.connection.cursor() as cursor:
    #         cursor.execute(f"""SELECT {key} FROM text WHERE id='{id}';""")
    #         message = cursor.fetchall()
    #         return str(list(message[0].values())[0])

    def get_text_for_all_lang(self, key : str)-> list[str]:
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute(f"""SELECT {key} FROM text;""")
                text = cursor.fetchall()
                return list( text)

        except Exception as e:
            print(e)
            return list()
        finally:
            self.disconnect()  


    # def get_advices_list(self):
    #     with self.connection.cursor() as cursor:
    #         cursor.execute(f"""SHOW COLUMNS FROM text;""")
    #         message = cursor.fetchall()
    #         return list(filter(lambda x: "advice" in x ,list(map(lambda x: x["Field"],message))))          

    def update_text_table(self, key: str, text: str, lang: str = "en")-> bool:
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                query = (f"""UPDATE text SET {key} = %s WHERE lang = %s;""")
                params = (text, lang)
                cursor.execute(query, params)
                self.connection.commit()
                return True

        except Exception as e:
            print(e)
            return False
        finally:
            self.disconnect()  


   
    #menus

    def set_start_data_menus(self)-> None:
        try:
            menus = pd.read_excel('data/excel_tables/menus.xlsx').to_numpy()
            self.connect()
            with self.connection.cursor() as cursor:
                query = """INSERT INTO menus (id, message, button_name, message_ru, 
                button_name_ru, message_fr, button_name_fr, message_ar, button_name_ar, 
                message_ch, button_name_ch) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

                params = [(int(elems[0][6:]), elems[1], elems[2], 
                           elems[3], elems[4], elems[5], elems[6], 
                           elems[7], elems[8], elems[9], elems[10])    
                           for elems in menus]

                cursor.executemany(query, params)

                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(e)
            print("Failed to load data into menus")
        finally:
            self.disconnect()

    def get_menus_text(self)-> list[str]:
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM menus;")
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(e)
            return []
        finally:
            self.disconnect()



#     def add_new_action_describtion(self, descriptions, lang = "en")-> int:
#         with self.connection.cursor() as cursor:
#             if(lang == "en"):
#                 cursor.execute(f"""INSERT INTO menus(message, button_name) 
#                 VALUES('{descriptions[0]}', '{descriptions[1]}');""")
#             else:
#                 cursor.execute(f"""INSERT INTO menus(message_{lang}, button_name_{lang}) 
#                 VALUES('{descriptions[0]}', '{descriptions[1]}');""")
#             self.connection.commit() 
#             cursor.execute(f"""SELECT LAST_INSERT_ID();""")
#             id = cursor.fetchall()
#             return int(id[0]['LAST_INSERT_ID()'])         

# #для упрощения заменить столбец на en
#     def get_message(self, id, lang = "en"):
#         with self.connection.cursor() as cursor:
#             if(lang == "en"):
#                 cursor.execute(f"""SELECT message FROM menus WHERE id='{id}';""")
#             else:
#                 cursor.execute(f"""SELECT message{"_" + lang} FROM menus WHERE id='{id}';""")
#             message = cursor.fetchall()
#             return str(list(message[0].values())[0])

#     def get_button_name(self, id, lang = "en"):
#         with self.connection.cursor() as cursor:
#             if(lang == "en"):
#                 cursor.execute(f"""SELECT button_name FROM menus WHERE id='{id}';""")
#             else:
#                 cursor.execute(f"""SELECT button_name{"_" + lang} FROM menus WHERE id='{id}';""")
#             button_name = cursor.fetchall()
#             return str(list(button_name[0].values())[0])

    def update_message(self, id, msg, lang = "en"):
        try:
            if(lang == "en"):
                self.connect()
                with self.connection.cursor() as cursor:
                    query = ("UPDATE menus SET message = %s WHERE id = %s;")
                    params = (msg, id)
                    cursor.execute(query, params)
                    self.connection.commit()
                    return True
            else:
                self.connect()
                with self.connection.cursor() as cursor:
                    query = (f"""UPDATE menus SET message{"_" + lang} = %s WHERE id = %s;""")
                    params = (msg, id)
                    cursor.execute(query, params)
                    self.connection.commit()
                    return True
        except Exception as e:
            print(e)
            return False
        finally:
            self.disconnect()  

    def update_button_name(self, id, button_name, lang = "en"):
        try:
            if(lang == "en"):
                self.connect()
                with self.connection.cursor() as cursor:
                    query = ("UPDATE menus SET button_name = %s WHERE id = %s;")
                    params = (button_name, id)
                    cursor.execute(query, params)
                    self.connection.commit()
                    return True
            else:
                self.connect()
                with self.connection.cursor() as cursor:
                    query = (f"""UPDATE menus SET button_name{"_" + lang} = %s WHERE id = %s;""")
                    params = (button_name, id)
                    cursor.execute(query, params)
                    self.connection.commit()
                    return True
        except Exception as e:
            print(e)
            return False
        finally:
            self.disconnect()  




    #users

    def add_user(self, id: int, username: str, lang = 'en', is_admin = False)-> bool:
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                query = "INSERT INTO users(id, username, language, is_admin) VALUES (%s, %s, %s, %s);"
                params = (id, username, lang, is_admin)
                cursor.execute(query,params)
                self.connection.commit()
                return True
        except Exception as e:
            self.connection.rollback()
            print(e)
            return False
        finally:
            self.disconnect()


    def check_user(self, id: int)-> bool:
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                query = "SELECT id FROM users WHERE id = %s;"
                params = (id,)
                cursor.execute(query,params)
                is_exists = cursor.fetchall()
                return bool(len(is_exists))
        except Exception as e:
            self.connection.rollback()
            print(e)
            return False
        finally:
            self.disconnect()


    def check_admin(self, id: int) -> bool: 
        try: 
            self.connect() 
            with self.connection.cursor() as cursor: 
                query = "SELECT is_admin FROM users WHERE id = %s;" 
                params = (id,) 
                cursor.execute(query, params) 
                is_admin = cursor.fetchone() 
                return bool(is_admin[0]) 
        except Exception as e: 
            print(e) 
            return False 
        finally: 
            self.disconnect()

    def get_lang(self, id): 
        try: 
            self.connect() 
            with self.connection.cursor() as cursor: 
                query = "SELECT language FROM users WHERE id = %s;" 
                params = (id,) 
                cursor.execute(query, params) 
                result = cursor.fetchone()
                return result[0] 
        except Exception as e: 
            print(e) 
            return None 
        finally: 
            self.disconnect()

    def update_lang(self, id, lang = 'en'): 
        try: 
            self.connect() 
            with self.connection.cursor() as cursor: 
                query = "UPDATE users SET language = %s WHERE id = %s;" 
                params = (lang, id) 
                cursor.execute(query, params) 
                self.connection.commit() 
        except Exception as e: 
            self.connection.rollback() 
            print(e) 
        finally: 
            self.disconnect()

    def del_user(self, id): 
        try: 
            self.connect() 
            with self.connection.cursor() as cursor: 
                query = "DELETE FROM users WHERE id = %s;" 
                params = (id,) 
                cursor.execute(query, params) 
                self.connection.commit() 
        except Exception as e: 
            self.connection.rollback() 
            print(e) 
        finally: 
            self.disconnect()

    def del_all_users(self): 
        try: 
            self.connect() 
            with self.connection.cursor() as cursor: 
                query = "DELETE FROM users WHERE is_admin = %s;" 
                params = (False,) 
                cursor.execute(query, params) 
                self.connection.commit() 
        except Exception as e: 
            self.connection.rollback() 
            print(e) 
        finally: 
            self.disconnect()

    def get_all_users_id(self)-> list[int]: 
        try: 
            self.connect() 
            with self.connection.cursor() as cursor: 
                query = "SELECT id FROM users WHERE is_admin = %s;" 
                params = (False,) 
                cursor.execute(query, params) 
                users = cursor.fetchall()
                return list(map(lambda user: user[0],users))
        except Exception as e: 
            print(e) 
            return []
        finally: 
            self.disconnect()

    def get_all_admins_id(self)-> list[int]: 
        try: 
            self.connect() 
            with self.connection.cursor() as cursor: 
                query = "SELECT id FROM users WHERE is_admin = %s;" 
                params = (True,) 
                cursor.execute(query, params) 
                admins = cursor.fetchall()
                return list(map(lambda admin: admin[0],admins))
        except Exception as e: 
            print(e) 
            return []
        finally: 
            self.disconnect()

    def add_admin_by_id(self ,id: int)-> bool: 
        try:  
            if self.check_user(id): 
                self.connect()
                with self.connection.cursor() as cursor: 
                    query = "UPDATE users SET is_admin = %s WHERE id = %s;" 
                    params = (True, id) 
                    cursor.execute(query, params) 
                    self.connection.commit()
            else:
                self.add_user(id, lang="ru", is_admin=True) 
            return True
        except Exception as e: 
            print(e) 
            return False
        finally: 
            self.disconnect()

    def del_admin_by_id(self ,id: int)-> bool: 
        try:  
            if self.check_user(id): 
                self.connect()
                with self.connection.cursor() as cursor: 
                    query = "UPDATE users SET is_admin = %s WHERE id = %s;" 
                    params = (False, id)
                    cursor.execute(query, params) 
                    self.connection.commit()
            else:
                self.add_user(id, lang="ru", is_admin=True) 
            return True
        except Exception as e: 
            print(e) 
            return False
        finally: 
            self.disconnect()


    #telegram_questions
    def add_new_question(self, user_id: int, question: str):
        try: 
            question_datetime = datetime.datetime.now()
            self.connect() 
            with self.connection.cursor() as cursor:  
                query = "INSERT INTO telegram_questions(user_id, question, question_datetime) VALUES (%s, %s, %s);" 
                params = (user_id, question, question_datetime) 
                cursor.execute(query, params) 
                self.connection.commit() 
        except Exception as e: 
            self.connection.rollback() 
            print(e) 
        finally: 
            self.disconnect()


    def answer_question(self, id: int, answer: str)-> bool:
        try: 
            answer_datetime = datetime.datetime.now()
            self.connect() 
            with self.connection.cursor() as cursor:  
                query = "UPDATE telegram_questions SET answer = %s, answer_datetime = %s WHERE id = %s;"
                params = (answer, answer_datetime, id)
                cursor.execute(query, params) 
                self.connection.commit() 
                return True
        except Exception as e: 
            print(e) 
            return False
        finally: 
            self.disconnect()


    def get_new_questions(self)-> list[tuple]:
        try: 
            self.connect() 
            with self.connection.cursor() as cursor:  
                cursor.execute("""SELECT id, question FROM telegram_questions WHERE answer IS NULL ORDER BY question_datetime;""") 
                questions = cursor.fetchall()
                return questions
        except Exception as e: 
            print(e)
            return list() 
        finally: 
            self.disconnect()

         
    def get_questions_by_user_id(self, user_id: int)-> list[tuple]:
        try: 
            self.connect() 
            with self.connection.cursor() as cursor:  
                query = "SELECT question, id FROM telegram_questions WHERE user_id = %s ORDER BY question_datetime;"
                params = (user_id, ) 
                cursor.execute(query, params)
                questions = cursor.fetchall()
                return questions
        except Exception as e: 
            print(e)
            return list() 
        finally: 
            self.disconnect()


    def get_question_by_id(self, question_id: int)-> str:
        try: 
            self.connect() 
            with self.connection.cursor() as cursor:  
                query = "SELECT question FROM telegram_questions WHERE id = %s;"
                params = (question_id, ) 
                cursor.execute(query, params)
                questions = cursor.fetchone()
                return questions[0]
        except Exception as e: 
            print(e)
            return None
        finally: 
            self.disconnect() 

    def get_answer_by_id(self, question_id: int)-> str:
        try: 
            self.connect() 
            with self.connection.cursor() as cursor:  
                query = "SELECT answer FROM telegram_questions WHERE id = %s;"
                params = (question_id, ) 
                cursor.execute(query, params)
                questions = cursor.fetchone()
                return questions[0]
        except Exception as e: 
            print(e)
            return None
        finally: 
            self.disconnect() 

    
    def get_user_by_id(self, id: int)-> int:
        try: 
            self.connect() 
            with self.connection.cursor() as cursor:  
                query = "SELECT user_id FROM telegram_questions WHERE id = %s;"
                params = (id, ) 
                cursor.execute(query, params)
                questions = cursor.fetchone()
                return questions[0]
        except Exception as e: 
            print(e)
            return None
        finally: 
            self.disconnect() 
 

 #forms
    def add_new_form(self, user_id: int, form_dict: dict)-> bool:
        try: 
            apply_date = datetime.datetime.now()
            birth_date = datetime.datetime.strptime(form_dict["birth_date"], "%d.%m.%Y").date()
            form_dict["apply_date"] = apply_date
            form_dict["birth_date"] = birth_date
            self.connect() 
            with self.connection.cursor() as cursor:  
                columns = ", ".join(form_dict.keys()) 
                values = ", ".join(["%s"] * (len(form_dict) + 1))
                query = f"""INSERT INTO forms(user_id, {columns}) VALUES({values});""" 
                params = list()
                params.append(user_id)
                params += form_dict.values()
                cursor.execute(query, params) 
                self.connection.commit() 
                return True
        except Exception as e: 
            print(e) 
            return False
        finally: 
            self.disconnect()

    # def update_form_element(self, form_id: int, column: str, value: object)-> bool:
    #     try: 
    #         self.connect() 
    #         with self.connection.cursor() as cursor:  
    #             query = "UPDATE forms SET {column} = '{value}' WHERE form_id = {form_id};"
    #             params = (elem, value, form_id) 
    #             cursor.execute(query, params) 
    #             self.connection.commit() 
    #             return True
    #     except Exception as e: 
    #         print(e) 
    #         return False
    #     finally: 
    #         self.disconnect()
    #     with self.connection.cursor() as cursor:
    #         cursor.execute(f"""UPDATE forms SET {column} = '{value}' WHERE form_id = {form_id};""")
    #         self.connection.commit()  


    def get_all_forms(self):
        with self.connection.cursor() as cursor:
            cursor.execute(f"""SELECT form_id FROM forms;""")             
            forms = cursor.fetchall()
            return list(map(lambda x: x['form_id'],forms))
    # не забыть отсортировать по дате
        

    def get_new_forms(self)-> list[int]:
        try: 
            self.connect() 
            with self.connection.cursor() as cursor:  
                cursor.execute("""SELECT form_id FROM forms WHERE is_reviewed = False ORDER BY apply_date;""") 
                forms = cursor.fetchall()
                return list(map(lambda form: form[0], forms))
        except Exception as e: 
            print(e)
            return list() 
        finally: 
            self.disconnect()


    def get_all_elem_by_form_id(self, form_id)-> tuple:
        try: 
            self.connect() 
            with self.connection.cursor() as cursor:  
                query = "SELECT * FROM forms WHERE form_id = %s;"
                params = (form_id, ) 
                cursor.execute(query, params) 
                form = cursor.fetchone()
                return form
        except Exception as e: 
            print(e) 
            return list()
        finally: 
            self.disconnect()


    def get_elem_by_id(self, elem, form_id):
        try: 
            self.connect() 
            with self.connection.cursor() as cursor:  
                query = f"SELECT {elem} FROM forms WHERE form_id = %s;"
                params = (form_id, ) 
                cursor.execute(query, params) 
                form = cursor.fetchone()
                return form[0]
        except Exception as e: 
            print(e) 
            return list()
        finally: 
            self.disconnect()



    def get_forms_by_user_id(self, user_id):   
        try: 
            self.connect() 
            with self.connection.cursor() as cursor:  
                query = "SELECT form_id FROM forms WHERE user_id = %s ORDER BY apply_date;"
                params = (user_id, ) 
                cursor.execute(query, params) 
                forms = cursor.fetchall()
                return list(forms[0])
        except Exception as e: 
            print(e) 
            return list()
        finally: 
            self.disconnect()

        


    def add_new_form_by_id(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(f"""INSERT INTO forms(user_id) VALUES({user_id});""")             
            self.connection.commit()

    def update_elem_by_id(self, elem: str, value: object, form_id: int)-> bool:
        try: 
            self.connect() 
            with self.connection.cursor() as cursor:  
                query = f"UPDATE forms SET {elem} = %s WHERE form_id = %s;"
                params = (value, form_id) 
                cursor.execute(query, params) 
                self.connection.commit() 
                return True
        except Exception as e: 
            print(e) 
            return False
        finally: 
            self.disconnect()
 
    # def set_comment_admin_NULL(self, form_id):
    #     try: 
    #         self.connect() 
    #         with self.connection.cursor() as cursor:  
    #             query = "UPDATE forms SET admin_comment = NULL ;"
    #             params = (elem, value, form_id) 
    #             cursor.execute(query, params) 
    #             self.connection.commit() 
    #             return True
    #     except Exception as e: 
    #         print(e) 
    #         return False
    #     finally: 
    #         self.disconnect()
    #     with self.connection.cursor() as cursor:
    #         cursor.execute(f"""UPDATE forms SET admin_comment = NULL;""")             
    #         self.connection.commit()   
#переименовать в update

    # def set_form_status_reviewed(self, form_id):
    #     with self.connection.cursor() as cursor:
    #         cursor.execute(f"""UPDATE forms SET is_reviewed = True WHERE form_id = {form_id};""")             
    #         self.connection.commit()        

    

    


    













# from config import host, user, password, database
# db = Database(host, user, password, database)

# a = db.get_text()
# print(a)

    

