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

df_dev = create_dev_change_columns(df_dev, dev_config)

missing = df_dev["change_over_20_years"].isna()

if missing.any():
    print(
        df_dev.loc[missing, ["country_name", "indicator_name"]]
        .sort_values(["indicator_name", "country_name"])
    )

    print(f"\nZeilen insgesamt: {df_dev.shape[0]}")