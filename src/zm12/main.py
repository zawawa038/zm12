import datetime
import typer
import tweepy
from zm12 import mathtools
from zm12 import vegetable
from . import demo
from . import gtrends
from . import tweet

app = typer.Typer()


@app.callback()
def callback():
    """
    A Collection of Useful Commands
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
def gtds(
    keyword: str = typer.Argument("Google", help="検索キーワード(複数語は間にスペース)"),
    timeframe: str = typer.Option("today 1-m", "--timeframe", "-t", help="時間範囲 (例: today_1-m, today_3-m, today_12-m, all)"),
    geo: str = typer.Option("JP", "--geo", "-g", help="地域コード (例:JP, US, GB)")
):
    if '_' in keyword:
        keyword = keyword.replace('_', ' ')
    if '_' in timeframe:
        timeframe = timeframe.replace('_', ' ')

    
    typer.echo(gtrends.get_search_volume(keyword, timeframe, geo))
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

@app.command()
def x_count(
    keyword: str = typer.Argument(..., help="検索キーワード"),
    days: int = typer.Option(7, "--days", "-d", help="検索期間（日数）"),
    max_results: int = typer.Option(100, "--max-results", "-m", help="最大取得数")
):
    # 上記のXTweetCounterクラスを使用
    config = load_config()
    counter = XTweetCounter(bearer_token=config['bearer_token'])
    stats = counter.get_tweet_count(keyword, days)
    counter.display_results(stats)