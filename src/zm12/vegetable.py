#!/usr/bin/env python3
import argparse
import sys

# 野菜の栄養価データ
# 実際のアプリケーションではより詳細なデータベースや外部APIを使用するとよいでしょう
VEGETABLE_NUTRITION = {
    "にんじん": {
        "カロリー": "41 kcal/100g",
        "ビタミンA": "高い（β-カロテン）",
        "ビタミンC": "中程度",
        "カリウム": "高い",
        "食物繊維": "多い"
    },
    "ほうれん草": {
        "カロリー": "23 kcal/100g",
        "ビタミンA": "高い",
        "ビタミンC": "高い",
        "鉄分": "高い",
        "葉酸": "高い",
        "マグネシウム": "多い"
    },
    "トマト": {
        "カロリー": "18 kcal/100g",
        "ビタミンC": "高い",
        "カリウム": "中程度",
        "リコピン": "多い",
        "抗酸化物質": "多い"
    },
    "じゃがいも": {
        "カロリー": "76 kcal/100g",
        "炭水化物": "高い",
        "ビタミンC": "中程度",
        "カリウム": "高い",
        "ビタミンB6": "中程度"
    },
    "キャベツ": {
        "カロリー": "23 kcal/100g",
        "ビタミンC": "高い",
        "ビタミンK": "高い",
        "食物繊維": "中程度",
        "葉酸": "中程度"
    },
    "ブロッコリー": {
        "カロリー": "34 kcal/100g",
        "ビタミンC": "非常に高い",
        "ビタミンK": "高い",
        "葉酸": "高い",
        "食物繊維": "多い"
    },
    "たまねぎ": {
        "カロリー": "40 kcal/100g",
        "ビタミンC": "中程度",
        "食物繊維": "中程度",
        "フラボノイド": "多い",
        "カリウム": "中程度"
    },
    "なす": {
        "カロリー": "25 kcal/100g",
        "食物繊維": "中程度",
        "ナスニン": "多い",
        "ポリフェノール": "中程度",
        "カリウム": "中程度"
    },
    "きゅうり": {
        "カロリー": "15 kcal/100g",
        "水分": "非常に高い",
        "ビタミンK": "中程度",
        "カリウム": "低い",
        "食物繊維": "低い"
    },
    "大根": {
        "カロリー": "18 kcal/100g",
        "ビタミンC": "中程度",
        "葉酸": "低い",
        "カリウム": "中程度",
        "消化酵素": "多い"
    }
}

def main():
    parser = argparse.ArgumentParser(description='野菜の栄養価を表示するプログラム')
    parser.add_argument('vegetable', help='栄養価を知りたい野菜の名前')
    parser.add_argument('-l', '--list', action='store_true', help='登録されている全ての野菜の一覧を表示')
    args = parser.parse_args()
    
    # 一覧表示オプションが指定された場合
    if args.list:
        print("登録されている野菜一覧:")
        for veg in sorted(VEGETABLE_NUTRITION.keys()):
            print(f"- {veg}")
        return
    
    # 指定された野菜の栄養価を表示
    vegetable = args.vegetable
    
    if vegetable in VEGETABLE_NUTRITION:
        print(f"===== {vegetable}の栄養価 =====")
        for nutrient, value in VEGETABLE_NUTRITION[vegetable].items():
            print(f"{nutrient}: {value}")
    else:
        print(f"エラー: '{vegetable}'の栄養価データが見つかりません。")
        print("登録されている野菜を確認するには '-l' または '--list' オプションを使用してください。")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
