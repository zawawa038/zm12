import datetime
import typer
from pathlib import Path #for anl_csv
from typing import Optional #for anl_csv
from typing import Tuple #for anl_csv
from zm12 import mathtools
from zm12 import vegetable
from . import demo
from . import gtrends
from . import csv_vslz #for anl_csv

app = typer.Typer()


@app.callback()
def callback():
    """
    A Collection of Useful Commands
    """
    
@app.command()
def anlz_csv(
    csv_file: Path = typer.Argument(..., help="CSVファイルのパス", exists=True),
    output_dir: str = typer.Option("plots", "--p", help="出力ディレクトリ"),
    figsize: str = typer.Option("12,4", help="図のサイズ (幅,高さ)"),
    show_only: bool = typer.Option(False, "--show", "--s", help="ファイル保存せずに表示のみ"),
    category: str = typer.Option(None, "--category", "--c", help="分類に使用する列名を指定（複数の場合はカンマ区切り）"),
    plot_type: str = typer.Option("all", "--plot-type", "--t", help="プロットの種類 (all/hist/box/violin)"),
    exclude: str = typer.Option(None, "--exclude", "--e", help="除外する列名（複数の場合はカンマ区切り）")
):
    """CSVファイルの数値変数を可視化"""
    try:
        w, h = map(int, figsize.split(','))
        typer.echo(csv_vslz.visualize_csv_data(str(csv_file), output_dir, (w, h), show_only, category, plot_type, exclude))
    except ValueError:
        typer.echo("エラー: figsizeは '幅,高さ' の形式で指定してください（例: '12,4'）", err=True)
        raise typer.Exit(1)
"""
用例：
# 単一列での分類
python csv_visualizer.py data.csv --category "性別"

# 複数列での分類（性別と年齢層の組み合わせ）
python csv_visualizer.py data.csv --category "性別,年齢層"

# 3つの列での分類（地域、部署、役職の組み合わせ）
python csv_visualizer.py employee_data.csv --category "地域,部署,役職"

# 複数列 + 表示のみ
python csv_visualizer.py sales_data.csv --category "地域,商品カテゴリ" --show
"""

"""
if __name__ == "__main__":
    app()
"""

@app.command()
def now():
    """
    Show local date and time
    """
    today = datetime.datetime.today()
    typer.echo(today.strftime('%A, %B %d, %Y'))


@app.command()
def gcd(x: int, y: int):
    """
    Greatest Common Divisor
    """
    typer.echo(mathtools.gcd(x, y))

@app.command()
def lcm(x: int, y: int):
    '''
    最小公倍数を求める
    '''
    typer.echo(mathtools.lcm(x, y))

@app.command()
def main(x: str):
    '''
    野菜の名前を引数にその栄養価を出力する
    ＊現在使用不能
    '''
    typer.echo(vegetable.main(x))

@app.command()
def hello(name: str= "Masaya"):
    typer.echo(demo.hello(name))

@app.command()
def gsv(
    keyword: str = typer.Argument(..., help="検索キーワード"),
    timeframe: str = typer.Option(
        "today 1-m", 
        "--timeframe", 
        "-t", 
        help="時間範囲 (デフォルト: today 1-m)"
    ),
    geo: str = typer.Option(
        "JP", 
        "--geo", 
        "-g", 
        help="地域コード (デフォルト: JP)"
    ),
    details: bool = typer.Option(
        False, 
        "--details", 
        "-d", 
        help="詳細データを表示"
    ),
    csv: Optional[str] = typer.Option(
        None, 
        "--csv", 
        "-c", 
        help="CSVファイルに出力 (ファイル名を指定)"
    ),
    exclude_partial: bool = typer.Option(
        False, 
        "--exclude-partial", 
        help="CSVからisPartial列を除外"
    ),
    completed_only: bool = typer.Option(
        False,
        "--completed-only",
        help="完全なデータのみ保存（部分的データの行を除外）"
    ),
    csv_folder: str = typer.Option(
        "google_trends_data",
        "--csv-folder",
        help="CSV保存用フォルダ名（デフォルト: google_trends_data）"
    ),
    date_folder: bool = typer.Option(
        False,
        "--date-folder",
        help="日付別サブフォルダに保存（YYYY-MM-DD形式）"
    )
):
    if '_' in keyword:
        keyword = keyword.replace('_', ' ')
    if '_' in timeframe:
        timeframe = timeframe.replace('_', ' ')
    
    """Google Trendsから検索数を取得して表示します"""
    
    typer.echo(f"Google Trendsから '{keyword}' の検索数を取得しています...")
    
    # 既存のファイルの関数を呼び出し
    data = gtrends.get_search_volume(keyword, timeframe, geo)
    
    if data is not None:
        # 既存のファイルの表示関数を呼び出し
        gtrends.display_results(data, keyword, details)
        
        # CSVファイルに出力
        if csv:
            try:
                # 保存用フォルダの作成
                folder_path = Path(csv_folder)
                folder_path.mkdir(exist_ok=True)
                
                # フルパスの作成
                csv_path = folder_path / csv
                
                save_data = data.copy()  # 元データを保持
                excluded_rows = 0
                
                # 部分的データ（行）の除外
                if completed_only and 'isPartial' in save_data.columns:
                    original_count = len(save_data)
                    save_data = save_data[save_data['isPartial'] == False]
                    excluded_rows = original_count - len(save_data)
                
                # isPartial列の除外
                if (exclude_partial or completed_only) and 'isPartial' in save_data.columns:
                    save_data = save_data.drop(columns=['isPartial'])
                
                # 保存
                save_data.to_csv(csv_path, encoding='utf-8-sig')
                
                # 保存結果の表示
                message = f"\nデータを '{csv_path}' に保存しました"
                if excluded_rows > 0:
                    message += f"（{excluded_rows}件の部分的データを除外）"
                if exclude_partial or completed_only:
                    message += "（isPartial列を除外）"
                message += "。"
                
                # フォルダが新規作成された場合の通知
                if not folder_path.existed_before:
                    typer.echo(f"フォルダ '{csv_folder}' を作成しました。")
                
                typer.echo(message)
                
            except Exception as e:
                typer.echo(f"CSV保存エラー: {e}", err=True)
    else:
        raise typer.Exit(1)
    
"""
基本的な使用方法
zm12 gtds Google

オプションを指定
zm12 gtds Google --timeframe today_1-m --geo JP

短縮オプションも使用可能
zm12 gtds Google -t today_1-m -g JP

アンダースコアで複数語を表現
zm12 gtds Google_株価
"""