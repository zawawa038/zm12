import requests
from pathlib import Path
from io import StringIO
import pandas as pd
from bs4 import XMLParsedAsHTMLWarning
import warnings

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

def get_data(url, name, number :int =0):
    # utf-8でHTMLを取得
    response = requests.get(url)
    response.encoding = 'utf-8'

    # pandasでテーブルを読み込みリストに格納
    tables = pd.read_html(StringIO(response.text))

    # テーブルリストからデータフレームを取得
    df = tables[number]
    
    output_path = Path.cwd() / "gotten_data"
    if not output_path.exists():
            output_path.mkdir(parents=True, exist_ok=True)
            print(f"出力ディレクトリを作成しました: {output_path}")
    else:
            pass
            #print(f"既存の出力ディレクトリを使用します: {output_path}")
    # csvファイルに出力
    df.to_csv(output_path / f"{name}", index=False)

