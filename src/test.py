import pandas as pd
from src.preparations import load_config
from src.analysis import create_dev_change_columns

from src.paths import (
    EDUCATION_RAW,
    DEVELOPMENT_CONFIG,
    EDUCATION_CONFIG,
    EDUCATION_OUTPUT,
    DEVELOPMENT_OUTPUT,
    COUNTRY_INFO
)




df_edu = pd.read_csv(EDUCATION_OUTPUT, encoding="utf-8")
df_dev = pd.read_csv(DEVELOPMENT_OUTPUT, encoding="utf-8")

dev_config = load_config(DEVELOPMENT_CONFIG)

df_dev_armut = df_dev[df_dev["indicator_code"] == "VC.IHR.PSRC.P5"]

df_dev_armut = create_dev_change_columns(df_dev_armut, dev_config)

print(
    df_dev_armut["change_over_10_years"].notna().sum()
)