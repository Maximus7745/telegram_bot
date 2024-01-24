import translators as ts

def get_tranlate(text: str)-> str:
    try:
        text_translate = ts.translate_text(text, to_language="ru", str="google")
        if(text_translate):
            return text_translate
        else:
            return text
    except Exception as e:
        print(e)
        return text
