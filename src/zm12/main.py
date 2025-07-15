import datetime

import typer

from zm12 import mathtools

from zm12 import vegetable

from . import demo

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