import seaborn as sns
import pandas as pd
from faicons import icon_svg

# Import data from shared.py
from shared import app_dir, df

from shiny import App, reactive, render, ui

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_select("action", 
                        "活動の種類（6種類）", 
                            {"walk":"歩行（3メッツ）", 
                            "fastwalk":"早歩き（4メッツ）", 
                            "jog":"ジョギング（7メッツ）", 
                            "cycling":"自転車（4メッツ）", 
                            "updownstair":"階段昇降（5.5メッツ）",
                            "ballsports":"球技（約6メッツ）"
                            }
                         ),
        ui.input_radio_buttons("minutes_mode", "入力期間（分）", choices={"week":"週間合計", "days":"曜日ごと"}),
        ui.output_ui("input_section"),
        ui.input_action_button("add", "追加"),
        ui.input_action_button("reset", "リセット"),
        title="1週間の活動を登録",
    ),
    ui.layout_column_wrap(
        ui.value_box(
            "メッツ・時の合計（推奨:23以上）",
            ui.output_text("count"),
            showcase=icon_svg("earlybirds"),
        ),
        ui.value_box(
            "Average bill length",
            ui.output_text("bill_length"),
            showcase=icon_svg("ruler-horizontal"),
        ),
        fill=False,
    ),
    ui.layout_columns(
        ui.card(
            ui.card_header("追加履歴"),
            ui.output_data_frame("added_log"),
            full_screen=True,
        ),
        ui.card(
            ui.card_header("Penguin data"),
            ui.output_data_frame("summary_statistics"),
            full_screen=True,
        ),
    ),
    ui.include_css(app_dir / "styles.css"),
    title="Penguins dashboard",
    fillable=True,
)


def server(input, output, session):
    total_mets = reactive.value(0)
    df = pd.DataFrame(
                    columns=["種類", "時間", "週/曜日"],
                    index=None
            )    
    @render.ui
    def input_section():
        if input.minutes_mode() == "days":
            return ui.card(
                ui.card_header("活動の時間（分）"),
                ui.card_body(
                    ui.input_numeric("minutes_sun", "日", 0, min = 0, step = 5),
                    ui.input_numeric("minutes_mon", "月", 0, min = 0, step = 5),
                    ui.input_numeric("minutes_tue", "火", 0, min = 0, step = 5),
                    ui.input_numeric("minutes_wed", "水", 0, min = 0, step = 5),
                    ui.input_numeric("minutes_thu", "木", 0, min = 0, step = 5),
                    ui.input_numeric("minutes_fri", "金", 0, min = 0, step = 5),
                    ui.input_numeric("minutes_sat", "土", 0, min = 0, step = 5),
                    )
        ),
        else:
            return ui.card(
                ui.card_header("活動の時間（分）"),
                ui.card_body(
                    ui.input_numeric("minutes_week", "1週間", 0, min = 0, step = 5),
                )
            )
    @reactive.calc
    def filtered_df():
        filt_df = df[df["species"].isin(input.species())]
        filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
        return filt_df

    @reactive.effect
    @reactive.event(input.add, ignore_none = False)
    def adding():
        if input.minutes_mode() == "days": # 曜日ごと入力モードの場合
            minutes = input.minutes_sun() + input.minutes_mon() + input.minutes_tue() + input.minutes_wed() + input.minutes_thu() + input.minutes_fri() + input.minutes_sat()
        else:                              # 週間合計モードの場合
            minutes = input.minutes_week()
        
        mets_values = {
                "walk" : 3,
                "fastwalk" : 4,
                "jog" : 7,
                "cycling" : 4,
                "updownstair" : 5.5,
                "ballsports" : 6
        }

        mets = mets_values.get(input.action())
        mets_h = mets * minutes / 60   

        total_mets.set(total_mets() + mets_h)     

    @reactive.effect
    @reactive.event(input.reset, ignore_none = False)
    def initialize():
        total_mets.set(0)

    @render.text
    def count():
        return f"{round(total_mets(), 1)} メッツ・時"

    @render.text
    def bill_length():
        return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    @render.text
    def bill_depth():
        return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

    @render.data_frame
    def added_log():
        return print(df)

    @render.data_frame
    def summary_statistics():
        cols = [
            "species",
            "island",
            "bill_length_mm",
            "bill_depth_mm",
            "body_mass_g",
        ]
        return render.DataGrid(filtered_df()[cols], filters=True)


app = App(app_ui, server)
