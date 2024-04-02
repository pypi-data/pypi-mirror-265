# deepl_translator/translator.py

import requests

def translate_text(text, target_language, source_language, auth_key):
    """DeepL APIを使ってテキストを翻訳する関数"""
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": auth_key,
        "text": text,
        "target_lang": target_language,
        "source_lang": source_language
    }

    response = requests.post(url, data=params)
    translated_text = response.json()["translations"][0]["text"]

    return translated_text
