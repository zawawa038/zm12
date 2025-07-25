import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import warnings

# 日本語フォント設定
def setup_japanese_font():
    """日本語フォントを設定"""
    import matplotlib.font_manager as fm
    
    # 利用可能な日本語フォントを探す
    japanese_fonts = [
        'Noto Sans CJK JP',
        'Yu Gothic',
        'Meiryo',
        'Hiragino Sans',
        'AppleGothic',
        'Malgun Gothic',
        'SimHei'
    ]
    
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    
    for font in japanese_fonts:
        if font in available_fonts:
            plt.rcParams['font.family'] = font
            print(f"日本語フォントを設定しました: {font}")
            return
    
    # フォールバック: matplotlibのデフォルト日本語対応
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Takao', 'DejaVu Sans', 'Lucida Grande', 'Verdana', 'Geneva', 'Lucid', 'Arial', 'Helvetica', 'Avant Garde', 'sans-serif']
    
    # 負の値の表示も修正
    plt.rcParams['axes.unicode_minus'] = False
    print("デフォルトフォント設定を使用します")

# フォント設定を実行
setup_japanese_font()
warnings.filterwarnings('ignore')

def visualize_csv_data(csv_file_path, output_dir="plots", figsize=(12, 4), show_only=False):
    """
    CSVファイルの数値変数をヒストグラム、箱ひげ図、バイオリンプロットで可視化
    
    Parameters:
    -----------
    csv_file_path : str
        CSVファイルのパス
    output_dir : str
        出力ディレクトリ（デフォルト: "plots"）
    figsize : tuple
        図のサイズ（デフォルト: (12, 4)）
    show_only : bool
        Trueの場合は表示のみ、Falseの場合は保存（デフォルト: False）
    """
    
    try:
        # CSVファイルを読み込み
        df = pd.read_csv(csv_file_path)
        print(f"データを読み込みました: {csv_file_path}")
        print(f"データ形状: {df.shape}")
        
        # 出力ディレクトリを初期化（保存する場合のみ）
        if not show_only:
            output_path = Path(output_dir)
            if output_path.exists():
                import shutil
                shutil.rmtree(output_path)
                print(f"既存のディレクトリを削除しました: {output_path}")
            output_path.mkdir(exist_ok=True)
            print(f"出力ディレクトリを作成しました: {output_path}")
        
        # 数値列のみを抽出
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not numeric_columns:
            print("数値列が見つかりませんでした。")
            return
            
        print(f"数値列: {numeric_columns}")
        
        # 各数値列に対して3つのプロットを作成
        for column in numeric_columns:
            # 欠損値を除去
            data = df[column].dropna()
            
            if len(data) == 0:
                print(f"列 '{column}' にはデータがありません。スキップします。")
                continue
                
            print(f"列 '{column}' を処理中...")
            
            # 図を作成
            fig, axes = plt.subplots(1, 3, figsize=figsize)
            fig.suptitle(f'変数: {column}', fontsize=16, fontweight='bold')
            
            # 1. ヒストグラム
            axes[0].hist(data, bins=30, alpha=0.7, color='skyblue', edgecolor='black', linewidth=0.5)
            axes[0].set_title('ヒストグラム', fontsize=12)
            axes[0].set_xlabel(column, fontsize=10)
            axes[0].set_ylabel('頻度', fontsize=10)
            axes[0].grid(True, alpha=0.3)
            
            # 統計情報を追加
            mean_val = data.mean()
            std_val = data.std()
            axes[0].axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'平均: {mean_val:.2f}')
            axes[0].axvline(mean_val + std_val, color='orange', linestyle='--', alpha=0.7, label=f'±1σ')
            axes[0].axvline(mean_val - std_val, color='orange', linestyle='--', alpha=0.7)
            axes[0].legend(prop={'size': 9})
            
            # 2. 箱ひげ図
            box_plot = axes[1].boxplot(data, patch_artist=True)
            box_plot['boxes'][0].set_facecolor('lightgreen')
            box_plot['boxes'][0].set_alpha(0.7)
            axes[1].set_title('箱ひげ図', fontsize=12)
            axes[1].set_ylabel(column, fontsize=10)
            axes[1].grid(True, alpha=0.3)
            
            # 外れ値の数を表示
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            outliers = data[(data < Q1 - 1.5 * IQR) | (data > Q3 + 1.5 * IQR)]
            axes[1].text(0.5, 0.95, f'外れ値: {len(outliers)}個', 
                        transform=axes[1].transAxes, ha='center', va='top', fontsize=9,
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            # 3. バイオリンプロット
            violin_parts = axes[2].violinplot(data, positions=[1], showmeans=True, showmedians=True)
            for pc in violin_parts['bodies']:
                pc.set_facecolor('lightcoral')
                pc.set_alpha(0.7)
            axes[2].set_title('バイオリンプロット', fontsize=12)
            axes[2].set_ylabel(column, fontsize=10)
            axes[2].set_xticks([1])
            axes[2].set_xticklabels([column], fontsize=9)
            axes[2].grid(True, alpha=0.3)
            
            # 統計情報をテキストで追加
            stats_text = f'平均: {data.mean():.2f}\n中央値: {data.median():.2f}\n標準偏差: {data.std():.2f}'
            axes[2].text(0.02, 0.98, stats_text, transform=axes[2].transAxes, 
                        va='top', ha='left', fontsize=8,
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            # レイアウトを調整
            plt.tight_layout()
            
            if show_only:
                # 表示のみ
                plt.show()
            else:
                # ファイルを保存
                safe_column_name = "".join(c for c in column if c.isalnum() or c in (' ', '-', '_')).rstrip()
                filename = f"{safe_column_name}_visualization.png"
                filepath = output_path / filename
                plt.savefig(filepath, dpi=300, bbox_inches='tight')
                print(f"保存しました: {filepath}")
            
            # メモリを節約するため図を閉じる
            plt.close()
        
        # データの概要を出力
        print("\n=== データ概要 ===")
        print(df.describe())
        
        print(f"\n全ての可視化が完了しました。" + ("" if show_only else f" 出力先: {output_path}"))
        
    except FileNotFoundError:
        print(f"エラー: ファイル '{csv_file_path}' が見つかりません。")
    except pd.errors.EmptyDataError:
        print(f"エラー: ファイル '{csv_file_path}' が空です。")
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
"""
# 使用例（この部分はインポート時には実行されません）
if __name__ == "__main__":
    # テスト用のサンプルデータ作成
    import numpy as np
    
    # サンプルCSVを作成
    np.random.seed(42)
    sample_data = {
        '身長': np.random.normal(170, 10, 1000),
        '体重': np.random.normal(65, 15, 1000),
        '年齢': np.random.randint(20, 80, 1000),
        '年収': np.random.lognormal(14, 0.5, 1000)
    }
    sample_df = pd.DataFrame(sample_data)
    sample_df.to_csv('sample_data.csv', index=False)
    
    # 関数をテスト
    visualize_csv_data('sample_data.csv')
"""