import pandas as pd
import json

df_dev = pd.read_csv(r"data\raw\WDICSV.csv", encoding="utf-8")
df_edu = pd.read_csv(r"data\raw\EdStatsData.csv", encoding="utf-8")

frames = [df_dev, df_edu]
paths = [r"config\development_indicators.json", r"config\education_indicators.json"]
titles = ["development", "education"]

base_columns = ["Country Name", "Country Code", "Indicator Name", "Indicator Code"]

for df_raw, path, title in zip(frames, paths, titles):
    with open(path, "r", encoding="utf-8") as file:
        indicators_data = json.load(file)

    indicator_name_list = [indicators_data[indicator]["name"] for indicator in indicators_data]

    filter_relevant_indicators = df_raw["Indicator Name"].isin(indicator_name_list)

    df_relevant_indicators = df_raw[filter_relevant_indicators]

    year_cols = [col for col in df_relevant_indicators.columns if col.isdigit()]

    relevant_year_cols = []
    for year in year_cols:
        if df_relevant_indicators[year].notna().sum() > 0:
            relevant_year_cols.append(year)

    df_relevant_years = df_relevant_indicators[base_columns + relevant_year_cols]

    df_relevant_countries = df_relevant_years[~df_relevant_years[relevant_year_cols].isna().all(axis=1)]

    df_relevant_countries.to_csv(
        rf"data\processed\{title}_indicators.csv",
        index=False,
        encoding="utf-8"
    )