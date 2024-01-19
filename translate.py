# from googletrans import Translator


def get_tranlate(text: str)-> str:
    try:
        translator = Translator()
        lang = translator.detect(text).lang
        tranlate_text = translator.translate(text, src=lang, dest='ru')
        return tranlate_text
    except Exception as e:
        print(e)
        return None


