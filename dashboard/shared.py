from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent
df = pd.read_csv(app_dir / "penguins.csv")

def m_to_h(minutes:int):
    hour = minutes / 60
    return hour