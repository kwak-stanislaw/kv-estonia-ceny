import deep_translator
import pandas as pd

# Some need API key
# deep_translator.DeeplTranslator()
# deep_translator.GoogleTranslator()
# # deep_translator.PonsTranslator()
# deep_translator.BaiduTranslator()
# deep_translator.QcriTranslator()
# deep_translator.LibreTranslator()
# deep_translator.MicrosoftTranslator()
# deep_translator.LingueeTranslator()
# deep_translator.MyMemoryTranslator()
# deep_translator.PapagoTranslator()
# deep_translator.YandexTranslator()
# deep_translator.ChatGptTranslator()

def translate_text(text):
    if isinstance(text, str):
        translator = deep_translator.GoogleTranslator()#source="auto", target="pl")
        return translator.translate(text)
    return None

text = """Продаётся опель омега б рестайлинг 2.2 бензин автомат коробка. Состояние отличное, всё электроника работает отлично."""

df = pd.DataFrame({"text": [text]})
df["translation"] = df["text"].apply(translate_text)
print(df)

