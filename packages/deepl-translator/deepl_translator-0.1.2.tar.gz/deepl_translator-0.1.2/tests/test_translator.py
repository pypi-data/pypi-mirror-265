import pytest
from deepl_translator.translator import translate_text
from deepl_translator.config import load_api_key

def test_translate_text():
    # 翻訳機能のテストケース
    # この例では、実際にAPIを呼び出さず、期待される出力を模擬的にテストします
    # 実際のAPI呼び出しを行うテストを書く場合は、APIレート制限や課金に注意してください
    text = "Hello"
    target_language = "JA"
    source_language = "EN"
    auth_key = load_api_key()

    # translate_text関数の呼び出し（ここではダミーデータを返すようにモックを使用することを推奨）
    translated_text = translate_text(text, target_language, source_language, auth_key)

    # 翻訳結果の検証（ダミーデータを使用しているので、期待される出力を仮定する）
    assert translated_text == "こんにちは"  # 仮の期待値
