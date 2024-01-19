from aiogram.types import FSInputFile

def get_file(key: str)-> FSInputFile:
    return files[key]


def load_files()-> None:
    files["photo1705054721"] = FSInputFile('data/firtst_steps_in_ekb/ru/photo1705054721.jpeg')
    files["photo1705054721_1"] = FSInputFile('data/firtst_steps_in_ekb/ru/photo1705054721 (1).jpeg')
    files["first_steps_page1"] = FSInputFile('data/firtst_steps_in_ekb/en/first_steps_page1.jpeg')
    files["first_steps_page2"] = FSInputFile('data/firtst_steps_in_ekb/en/first_steps_page2.jpeg')
    files["Visa_application_form"] = FSInputFile('data/visa_docs/Visa_application_form.pdf')
    files["Visa_application_form_example"] = FSInputFile('data/visa_docs/Visa_application_form_example.pdf')

files = dict()
load_files()