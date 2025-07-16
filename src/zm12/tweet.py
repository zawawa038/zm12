#!/usr/bin/env python3
"""
X(旧Twitter)で特定のキーワードを含む投稿数を取得するプログラム

必要な準備:
1. X Developer Portalでアプリを作成
2. API Key, API Secret, Bearer Token, Access Token, Access Token Secretを取得
3. pip install tweepy
"""

import tweepy
import argparse
import os
import sys
from datetime import datetime, timedelta
import json
import time

class XTweetCounter:
    def __init__(self, bearer_token, api_key=None, api_secret=None, access_token=None, access_token_secret=None):
        """
        X API認証を初期化
        
        Args:
            bearer_token (str): Bearer Token
            api_key (str): API Key (Consumer Key)
            api_secret (str): API Secret (Consumer Secret)
            access_token (str): Access Token
            access_token_secret (str): Access Token Secret
        """
        self.bearer_token = bearer_token
        
        # v2 API用のクライアント（検索専用）
        self.client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            wait_on_rate_limit=True
        )
    
    def search_tweets(self, query, max_results=100, days_back=7):
        """
        キーワードを含むツイートを検索
        
        Args:
            query (str): 検索クエリ
            max_results (int): 取得する最大ツイート数（10-100）
            days_back (int): 過去何日分を検索するか（最大7日）
        
        Returns:
            list: ツイートデータのリスト
        """
        try:
            # 検索期間を設定（最大7日前まで）
            end_time = datetime.now()
            start_time = end_time - timedelta(days=min(days_back, 7))
            
            # 検索クエリを構築
            search_query = f"{query} -is:retweet lang:ja"  # リツイート除外、日本語のみ
            
            print(f"検索クエリ: {search_query}")
            print(f"検索期間: {start_time.strftime('%Y-%m-%d')} から {end_time.strftime('%Y-%m-%d')}")
            
            # ツイートを検索
            tweets = tweepy.Paginator(
                self.client.search_recent_tweets,
                query=search_query,
                max_results=min(max_results, 100),
                start_time=start_time,
                end_time=end_time,
                tweet_fields=['created_at', 'author_id', 'public_metrics', 'lang']
            ).flatten(limit=max_results)
            
            tweet_list = []
            for tweet in tweets:
                tweet_data = {
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at,
                    'author_id': tweet.author_id,
                    'retweet_count': tweet.public_metrics['retweet_count'],
                    'like_count': tweet.public_metrics['like_count'],
                    'reply_count': tweet.public_metrics['reply_count'],
                    'quote_count': tweet.public_metrics['quote_count']
                }
                tweet_list.append(tweet_data)
            
            return tweet_list
            
        except tweepy.TooManyRequests:
            print("Rate limit exceeded. Please wait and try again later.")
            return []
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            return []
    
    def get_tweet_count(self, query, days_back=7):
        """
        特定のキーワードを含むツイートの数を取得
        
        Args:
            query (str): 検索クエリ
            days_back (int): 過去何日分を検索するか
        
        Returns:
            dict: 統計情報
        """
        try:
            # 無料プランでは制限があるため、小さな値で検索
            tweets = self.search_tweets(query, max_results=100, days_back=days_back)
            
            if not tweets:
                return {
                    'keyword': query,
                    'count': 0,
                    'period_days': days_back,
                    'total_retweets': 0,
                    'total_likes': 0,
                    'average_engagement': 0
                }
            
            # 統計を計算
            total_retweets = sum(tweet['retweet_count'] for tweet in tweets)
            total_likes = sum(tweet['like_count'] for tweet in tweets)
            total_replies = sum(tweet['reply_count'] for tweet in tweets)
            total_quotes = sum(tweet['quote_count'] for tweet in tweets)
            
            engagement_rate = (total_likes + total_retweets + total_replies + total_quotes) / len(tweets)
            
            stats = {
                'keyword': query,
                'count': len(tweets),
                'period_days': days_back,
                'total_retweets': total_retweets,
                'total_likes': total_likes,
                'total_replies': total_replies,
                'total_quotes': total_quotes,
                'average_engagement': engagement_rate,
                'tweets': tweets[:10]  # 最新10件のサンプル
            }
            
            return stats
            
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            return None
    
    def display_results(self, stats):
        """
        検索結果を表示
        """
        if not stats:
            print("結果を取得できませんでした。")
            return
        
        print(f"\n=== X(Twitter) 投稿数統計: '{stats['keyword']}' ===")
        print(f"検索期間: 過去{stats['period_days']}日間")
        print(f"投稿数: {stats['count']}件")
        print(f"総リツイート数: {stats['total_retweets']:,}")
        print(f"総いいね数: {stats['total_likes']:,}")
        print(f"総返信数: {stats['total_replies']:,}")
        print(f"総引用数: {stats['total_quotes']:,}")
        print(f"平均エンゲージメント: {stats['average_engagement']:.1f}")
        
        if stats['tweets']:
            print(f"\n最新の投稿サンプル:")
            print("-" * 60)
            for i, tweet in enumerate(stats['tweets'][:5], 1):
                print(f"{i}. {tweet['created_at'].strftime('%Y-%m-%d %H:%M')}")
                print(f"   {tweet['text'][:100]}...")
                print(f"   👍{tweet['like_count']} 🔄{tweet['retweet_count']} 💬{tweet['reply_count']}")
                print()

def load_config():
    """
    設定ファイルまたは環境変数からAPI認証情報を読み込み
    """
    config = {
        'bearer_token': os.getenv('X_BEARER_TOKEN'),
        'api_key': os.getenv('X_API_KEY'),
        'api_secret': os.getenv('X_API_SECRET'),
        'access_token': os.getenv('X_ACCESS_TOKEN'),
        'access_token_secret': os.getenv('X_ACCESS_TOKEN_SECRET')
    }
    
    # config.jsonファイルからも読み込み可能
    try:
        with open('config.json', 'r') as f:
            file_config = json.load(f)
            for key, value in file_config.items():
                if config.get(key) is None:
                    config[key] = value
    except FileNotFoundError:
        pass
    
    return config

def main():
    parser = argparse.ArgumentParser(
        description='X(旧Twitter)で特定のキーワードを含む投稿数を取得',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用例:
  python x_counter.py "Python"
  python x_counter.py "AI" --days 3
  python x_counter.py "コロナ" --max-results 50
  
環境変数の設定:
  export X_BEARER_TOKEN="your_bearer_token"
  export X_API_KEY="your_api_key"
  export X_API_SECRET="your_api_secret"
  export X_ACCESS_TOKEN="your_access_token"
  export X_ACCESS_TOKEN_SECRET="your_access_token_secret"
  
または config.json ファイルを作成:
  {
    "bearer_token": "your_bearer_token",
    "api_key": "your_api_key",
    "api_secret": "your_api_secret",
    "access_token": "your_access_token",
    "access_token_secret": "your_access_token_secret"
  }
        '''
    )
    
    parser.add_argument('keyword', help='検索キーワード')
    parser.add_argument('--days', '-d', type=int, default=7, 
                       help='検索期間（日数、最大7日）')
    parser.add_argument('--max-results', '-m', type=int, default=100,
                       help='取得する最大ツイート数（10-100）')
    parser.add_argument('--save-json', '-s', 
                       help='結果をJSONファイルに保存')
    
    args = parser.parse_args()
    
    # 認証情報を読み込み
    config = load_config()
    
    if not config['bearer_token']:
        print("エラー: Bearer Tokenが設定されていません。")
        print("環境変数またはconfig.jsonファイルを設定してください。")
        sys.exit(1)
    
    # X API クライアントを初期化
    counter = XTweetCounter(
        bearer_token=config['bearer_token'],
        api_key=config['api_key'],
        api_secret=config['api_secret'],
        access_token=config['access_token'],
        access_token_secret=config['access_token_secret']
    )
    
    print(f"'{args.keyword}' を含む投稿を検索しています...")
    
    # ツイート数を取得
    stats = counter.get_tweet_count(args.keyword, args.days)
    
    # 結果を表示
    counter.display_results(stats)
    
    # JSONファイルに保存
    if args.save_json and stats:
        try:
            with open(args.save_json, 'w', encoding='utf-8') as f:
                # datetimeオブジェクトを文字列に変換
                stats_copy = stats.copy()
                for tweet in stats_copy['tweets']:
                    tweet['created_at'] = tweet['created_at'].isoformat()
                json.dump(stats_copy, f, ensure_ascii=False, indent=2)
            print(f"\n結果を '{args.save_json}' に保存しました。")
        except Exception as e:
            print(f"JSON保存エラー: {e}")

"""
if __name__ == "__main__":
    main()
    """