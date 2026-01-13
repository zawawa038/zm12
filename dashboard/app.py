from shiny import App, reactive, render, ui
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 市町村データ
municipalities_data = [
    {"name": "都島区", "reading": "みやこじまく", "type": "区", "parent": "大阪市"},
    {"name": "福島区", "reading": "ふくしまく", "type": "区", "parent": "大阪市"},
    # ... (他のデータ)
]

municipalities_df = pd.DataFrame(municipalities_data)

def generate_sample_data(start_year, end_year):
    """サンプル統計データを生成"""
    years = list(range(start_year, end_year + 1))
    np.random.seed(42)
    
    data = {
        'year': years,
        'turnout_rate': [45 + np.random.normal(0, 5) for _ in years],
        'total_voters': [80000 + i * 2000 + np.random.normal(0, 3000) for i in range(len(years))],
        'male_voters': [38000 + i * 1000 + np.random.normal(0, 1500) for i in range(len(years))],
        'female_voters': [42000 + i * 1000 + np.random.normal(0, 1500) for i in range(len(years))],
        'candidate_count': [25 + np.random.randint(-3, 4) for _ in years],
        'fixed_seats': [20 + np.random.randint(-1, 2) for _ in years]
    }
    
    data['candidate_ratio'] = [data['fixed_seats'][i] / data['candidate_count'][i] for i in range(len(years))]
    
    for key in ['turnout_rate', 'total_voters', 'male_voters', 'female_voters']:
        if key == 'turnout_rate':
            data[key] = [max(0, min(100, val)) for val in data[key]]
        else:
            data[key] = [max(0, int(val)) for val in data[key]]
    
    data['candidate_count'] = [max(1, val) for val in data['candidate_count']]
    data['fixed_seats'] = [max(1, min(val, data['candidate_count'][i])) for i, val in enumerate(data['fixed_seats'])]
    
    return pd.DataFrame(data)

# 統合されたUI
app_ui = ui.page_fluid(
    ui.h1("🗳️ 大阪府の選挙情報", 
          style="text-align: center; color: #1e40af; margin-bottom: 30px; padding: 20px; background-color: #f1f5f9; border-radius: 10px;"),
    
    # 市町村検索セクション
    ui.card(
        ui.card_header("市町村検索"),
        ui.layout_sidebar(
            ui.sidebar(
                ui.h3("検索条件"),
                ui.input_select(
                    "initial_letter",
                    "頭文字を選択:",
                    choices={
                        "": "すべて",
                        "あ": "あ行",
                        "か": "か行", 
                        "さ": "さ行",
                        "た": "た行",
                        "な": "な行",
                        "は": "は行",
                        "ま": "ま行",
                        "や": "や行",
                    },
                    selected=""
                ),
                ui.input_select(
                    "municipality_type",
                    "自治体種別:",
                    choices={
                        "": "すべて",
                        "区": "区",
                        "市": "市",
                        "町": "町",
                        "村": "村",
                    },
                    selected=""
                ),
                ui.input_text(
                    "name_filter",
                    "区市町村名で絞り込み:",
                    value="",
                    placeholder="区市町村名の一部を入力"
                ),
                ui.br(),
                ui.p(f"総登録数: {len(municipalities_df)}件")
            ),
            ui.output_data_frame("municipalities_table")
        )
    ),
    
    ui.br(),
    
    # 統計グラフセクション
    ui.card(
        ui.card_header("統計データ推移グラフ"),
        ui.layout_sidebar(
            ui.sidebar(
                ui.h3("表示設定"),
                ui.input_slider(
                    "year_range",
                    "表示年度範囲:",
                    min=2000,
                    max=2020,
                    value=[2010, 2020],
                    step=1,
                    sep=""
                ),
                ui.br(),
                ui.input_checkbox_group(
                    "selected_metrics",
                    "表示する統計項目を選択してください:",
                    choices={
                        "turnout_rate": "投票率 (%)",
                        "total_voters": "有権者数 (人)",
                        "candidate_ratio": "定数比候補者数",
                        "male_voters": "有権者数（男性）",
                        "female_voters": "有権者数（女性）"
                    },
                    selected=["turnout_rate"]
                ),
                ui.br(),
                ui.p("※ データはサンプルデータです。")
            ),
            ui.output_plot("statistics_plot")
        )
    )
)

def server(input, output, session):
    # 市町村検索機能
    @reactive.calc
    def filtered_municipalities():
        df = municipalities_df.copy()
        
        if input.initial_letter():
            hiragana_ranges = {
                "あ": ["あ", "い", "う", "え", "お"],
                "か": ["か", "き", "く", "け", "こ", "が", "ぎ", "ぐ", "げ", "ご"],
                "さ": ["さ", "し", "す", "せ", "そ", "ざ", "じ", "ず", "ぜ", "ぞ"],
                "た": ["た", "ち", "つ", "て", "と", "だ", "ぢ", "づ", "で", "ど"],
                "な": ["な", "に", "ぬ", "ね", "の"],
                "は": ["は", "ひ", "ふ", "へ", "ほ", "ば", "び", "ぶ", "べ", "ぼ", "ぱ", "ぴ", "ぷ", "ぺ", "ぽ"],
                "ま": ["ま", "み", "む", "め", "も"],
                "や": ["や", "ゆ", "よ"],
            }
            
            target_chars = hiragana_ranges.get(input.initial_letter(), [])
            df = df[df["reading"].str[0].isin(target_chars)]
        
        if input.municipality_type():
            df = df[df["type"] == input.municipality_type()]
        
        if input.name_filter():
            df = df[df["name"].str.contains(input.name_filter(), na=False)]
        
        return df.sort_values("reading").reset_index(drop=True)
    
    @render.data_frame
    def municipalities_table():
        df = filtered_municipalities()
        display_df = df[["name", "type", "reading"]].copy()
        display_df.columns = ["市町村名", "種別", "読み方"]
        
        return render.DataTable(
            display_df,
            height="400px",
            summary=f"検索結果: {len(display_df)}件",
            selection_mode="row"
        )
    
    # 統計グラフ機能
    @reactive.calc
    def filtered_data():
        year_range = input.year_range()
        start_year, end_year = year_range[0], year_range[1]
        return generate_sample_data(start_year, end_year)
    
    @render.plot
    def statistics_plot():
        selected_metrics = input.selected_metrics()
        data = filtered_data()
        
        if not selected_metrics:
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.text(0.5, 0.5, '表示項目を選択してください', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=16)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            return fig
        
        # (グラフ描画コードは元のまま)
        # ...省略...
        
        return fig

app = App(app_ui, server)