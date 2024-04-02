# deepl_translator/config.py

from dotenv import load_dotenv
import os

def load_api_key():
    """DeepL APIキーを.envファイルから読み込む関数"""
    load_dotenv()
    return os.getenv("DEEPL_API_KEY")
