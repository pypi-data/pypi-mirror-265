# deepl_translator/cli.py

import click
from .translator import translate_text
from .config import load_api_key

@click.command()
@click.option('--target', '-t', type=click.Choice(['JA', 'EN']), help='Target language: JA for Japanese, EN for English')
@click.option('--source', '-s', type=click.Choice(['JA', 'EN']), default=None, help='Source language: JA for Japanese, EN for English (optional)')
def main(target, source):
    """コマンドラインから翻訳タスクを実行する関数"""
    auth_key = load_api_key()  # APIキーの読み込み
    if not auth_key:
        click.echo("APIキーが設定されていません。.envファイルを確認してください。")
        return

    text = click.get_text_stream('stdin').read()  # 標準入力からテキストを読み取る
    translated_text = translate_text(text, target, source if source else 'auto', auth_key)  # 翻訳の実行
    click.echo(translated_text)  # 翻訳結果の出力


