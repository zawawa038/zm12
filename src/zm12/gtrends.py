#!/usr/bin/env python3
"""
Google Trendsから検索数を取得するコマンドラインプログラム
"""

import argparse
import sys
from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime, timedelta
import time

def get_search_volume(keyword, timeframe='today 12-m', geo='JP'):
    """
    Google Trendsから検索数を取得する関数
    
    Args:
        keyword (str): 検索キーワード
        timeframe (str): 時間範囲 (例: 'today 12-m', 'today 3-m', 'all')
        geo (str): 地域コード (例: 'JP'は日本, 'US'はアメリカ, ''は世界全体)
    
    Returns:
        pandas.DataFrame: 検索数データ
    """
    try:
        # TrendReqオブジェクトを作成
        pytrends = TrendReq(hl='ja-JP', tz=540)  # 日本時間設定
        
        # キーワードを設定
        pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo, gprop='')
        
        # 検索数データを取得
        data = pytrends.interest_over_time()
        
        if data.empty:
            print(f"キーワード '{keyword}' のデータが見つかりませんでした。")
            return None
            
        return data
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None

def display_results(data, keyword, show_details=False):
    """
    結果を表示する関数
    
    Args:
        data (pandas.DataFrame): 検索数データ
        keyword (str): 検索キーワード
        show_details (bool): 詳細表示するかどうか
    """
    if data is None:
        return
    
    print(f"\n=== Google Trends検索数: '{keyword}' ===")
    print(f"期間: {data.index[0].strftime('%Y-%m-%d')} から {data.index[-1].strftime('%Y-%m-%d')}")
    print(f"データポイント数: {len(data)}")
    
    # 基本統計
    search_values = data[keyword]
    print(f"\n基本統計:")
    print(f"  最大値: {search_values.max()}")
    print(f"  最小値: {search_values.min()}")
    print(f"  平均値: {search_values.mean():.2f}")
    print(f"  最新値: {search_values.iloc[-1]}")
    
    # 最大値の日付
    max_date = search_values.idxmax()
    print(f"  最大値の日付: {max_date.strftime('%Y-%m-%d')}")
    
    if show_details:
        print(f"\n詳細データ (最新10件):")
        print("-" * 40)
        for date, value in search_values.tail(10).items():
            print(f"{date.strftime('%Y-%m-%d')}: {value:3d}")

def main():
    parser = argparse.ArgumentParser(
        description='Google Trendsから検索数を取得します',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用例:
  python google_trends.py "Python プログラミング"
  python google_trends.py "コロナウイルス" --timeframe "today 3-m"
  python google_trends.py "iPhone" --geo "US" --details
  python google_trends.py "東京オリンピック" --timeframe "all"

時間範囲の指定:
  today 1-m    : 過去1ヶ月
  today 3-m    : 過去3ヶ月
  today 12-m   : 過去12ヶ月 (デフォルト)
  today 5-y    : 過去5年
  all          : 全期間

地域コード:
  JP : 日本 (デフォルト)
  US : アメリカ
  GB : イギリス
  ''  : 世界全体
        '''
    )
    
    parser.add_argument('keyword', help='検索キーワード')
    parser.add_argument('--timeframe', '-t', default='today 12-m', 
                       help='時間範囲 (デフォルト: today 12-m)')
    parser.add_argument('--geo', '-g', default='JP', 
                       help='地域コード (デフォルト: JP)')
    parser.add_argument('--details', '-d', action='store_true',
                       help='詳細データを表示')
    parser.add_argument('--csv', '-c', 
                       help='CSVファイルに出力 (ファイル名を指定)')
    
    args = parser.parse_args()
    
    print(f"Google Trendsから '{args.keyword}' の検索数を取得しています...")
    
    # 検索数データを取得
    data = get_search_volume(args.keyword, args.timeframe, args.geo)
    
    if data is not None:
        # 結果を表示
        display_results(data, args.keyword, args.details)
        
        # CSVファイルに出力
        if args.csv:
            try:
                data.to_csv(args.csv, encoding='utf-8-sig')
                print(f"\nデータを '{args.csv}' に保存しました。")
            except Exception as e:
                print(f"CSV保存エラー: {e}")
    else:
        sys.exit(1)

"""
if __name__ == "__main__":
    main()
"""