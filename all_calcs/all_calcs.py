from pathlib import Path
import pandas as pd
from utils.hilfsfunktionen import dump_json
from app.save_combinations import (
    create_analysis_key, 
    calculate_correlations,
)
from src.analysis import (
    create_development_dataframe, 
    create_education_dataframe,
    merge_dev_edu_data,
    select_dataframe,
    find_relevant_years,
)

def get_analysis_data(dev_indicator: str, edu_indicator: str, change_offset: int) -> tuple[str, str, int]:
    return dev_indicator, edu_indicator, change_offset


def merge_dev_edu_data(
    df_dev: pd.DataFrame,
    df_edu: pd.DataFrame, 
    change_offset: int
) -> pd.DataFrame:
    """
    Führt Entwicklungs- und Bildungs-Daten anhand des Landes zusammen.
    """

    return df_dev.merge(
        df_edu,
        on=["country_code", "country_name"],
        how="inner"
    ).dropna(
        subset=[
            f"change_over_{change_offset}_years",
            f"value_education_year_{change_offset}"
        ]
    )



def create_indicator_frame (indicator_code: str, frame_name: str = "edu", indicator_title: str = "indicator") -> pd.DataFrame:
    
    df = select_dataframe(frame_name)

    df_indicator = df[df["indicator_code"] == indicator_code]

    years = find_relevant_years(df_indicator)

    df_indicator[f"{indicator_title}_data_count"] = df_indicator[years].notna().sum(axis=1)

    df_indicator = df_indicator[
        df_indicator[f"{indicator_title}_data_count"] > 0
    ]

    relevant_columns = [
        'country_name',
        'country_code',
        'indicator_name',
        'indicator_code',
        f'{indicator_title}_data_count'
    ] + years

    return df_indicator[relevant_columns]


def create_analysis_frames (dev_indicator: str, edu_indicator: str, dev_config: dict, edu_config: dict):

    dev_indicator, edu_indicator_dict, change_offset = get_analysis_data()

    df_dev_raw = create_indicator_frame(dev_indicator, "dev")
    df_edu_raw = create_indicator_frame(edu_indicator, "edu")

    df_dev = create_development_dataframe(df_dev_raw, dev_config)
    df_edu = create_education_dataframe(df_edu_raw, edu_config)
    
    return df_dev, df_edu


def create_correlation_result(
    development_indicator: str,
    education_indicator: str,
    development_category: str,
    education_category: str,
    change_offset: int,
    analysis_df: pd.DataFrame
) -> dict:
    """
    Prüft, ob eine Korrelationsanalyse bereits existiert.
    Falls nicht, wird sie berechnet, in das Dictionary aufgenommen
    und dauerhaft gespeichert.

    Gibt immer das Analyse-Ergebnis zurück.
    """

    correlations = calculate_correlations(analysis_df, change_offset)

    correlation_result = {
        "development_indicator": development_indicator,
        "development_category": development_category["name"],
        "education_indicator": education_indicator,
        "education_category": education_category["name"],
     
        "change_offset": change_offset,

        "countries": correlations["n"],

        "pearson": {
            "r": correlations["pearson_r"],
            "p": correlations["pearson_p"]
        },

        "spearman": {
            "r": correlations["spearman_r"],
            "p": correlations["spearman_p"]
        }
    }

    return correlation_result


def main_function (education_config: dict, development_config: dict):

    dev_indicators = development_config["indicators"].keys()
    edu_indicators = education_config["indicators"].keys()

    for dev_indicator in dev_indicators:
        dev_frame_raw = create_indicator_frame(dev_indicator, "dev")
        for edu_indicator in edu_indicators:
            edu_frame_raw = create_indicator_frame(edu_indicator, "edu")
            create_analysis_frames()
            df_

    analysis_key = create_analysis_key(development_indicator, education_indicator, change_offset)