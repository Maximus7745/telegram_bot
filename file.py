from aiogram.types import FSInputFile
import os

def get_files(key: str)-> list[FSInputFile]:
    return files[key]


def load_files()-> None:

    files["first_steps_en"] = get_inputfile('data/firtst_steps_in_ekb/en/')
    files["first_steps_ru"] = get_inputfile('data/firtst_steps_in_ekb/ru/')
    files["visa_application_form"] = get_inputfile('data/visa_docs/')


def get_inputfile(path: str)-> list[FSInputFile]:
    files_list = list()
    list_dirs = os.listdir(path)
    for file in list_dirs:
        files_list.append(FSInputFile(path + file))
    
    return files_list



files = dict()
load_files()