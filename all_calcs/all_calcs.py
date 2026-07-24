import pandas as pd
import random
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

from src.preparations import load_config

from src.paths import EDUCATION_CONFIG, DEVELOPMENT_CONFIG, CORRELATION_RESULTS


def merge_dev_edu_data(
    df_dev: pd.DataFrame,
    df_edu: pd.DataFrame, 
    change_offset: int,
    lag_factor: int
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
            f"value_education_year_{change_offset}_factor_{lag_factor}"
        ]
    )

def create_indicator_frame (df: pd.DataFrame, indicator_code: str) -> pd.DataFrame:

    df_indicator = df[df["indicator_code"] == indicator_code].copy()

    years = find_relevant_years(df_indicator)

    df_indicator["indicator_data_count"] = df_indicator[years].notna().sum(axis=1)

    df_indicator = df_indicator[
        df_indicator["indicator_data_count"] > 0
    ]

    relevant_columns = [
        'country_name',
        'country_code',
        'indicator_name',
        'indicator_code',
        'indicator_data_count'
    ] + years

    return df_indicator[relevant_columns]


def create_correlation_result(
    development_indicator: str,
    education_indicator: str,
    development_category: str,
    education_category: str,
    change_offset: int,
    lag_factor: int,
    analysis_df: pd.DataFrame
) -> dict:

    correlations = calculate_correlations(analysis_df, change_offset, lag_factor)

    correlation_result = {
        "development_indicator": development_indicator,
        "development_category": development_category,
        "education_indicator": education_indicator,
        "education_category": education_category,
        "change_offset": change_offset,
        "lag_factor": lag_factor,
        "education_years": {
            "min": int(
                analysis_df[f"education_year_{change_offset}_factor_{lag_factor}"].min()
            ),
            "max": int(
                analysis_df[f"education_year_{change_offset}_factor_{lag_factor}"].max()
            )
        },
        "development_years": {
            "start_min": int(
                analysis_df[f"available_comparison_year_{change_offset}"].min()
            ),
            "start_max": int(
                analysis_df[f"available_comparison_year_{change_offset}"].max()
            ),
            "end_min": int(
                analysis_df["available_max_year"].min()
            ),
            "end_max": int(
                analysis_df["available_max_year"].max()
            )
        },

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


def get_category_name(config: dict, category_key: str) -> str:
    for category in config["meta_data"]["categories"]:
        if category["category"] == category_key:
            return category["name"]

    return category_key


def main_function():

    dev_config = load_config(DEVELOPMENT_CONFIG)
    edu_config = load_config(EDUCATION_CONFIG)

    dev_indicators = list(dev_config["indicators"].keys())
    edu_indicators = list(edu_config["indicators"].keys())

    min_available_countries = (
        edu_config["meta_data"]["min_available_countries"]
    )

    df_dev_origin = select_dataframe("dev")
    df_edu_origin = select_dataframe("edu")

    # -------------------------------------------------------
    # Entwicklungs-DataFrames vorberechnen
    # -------------------------------------------------------

    dev_frames = {}

    for dev_indicator in dev_indicators:

        df_dev_raw = create_indicator_frame(
            df_dev_origin,
            dev_indicator
        )

        dev_category = (
            dev_config["indicators"][dev_indicator]["category"]
        )

        dev_category_name = get_category_name(
            dev_config,
            dev_category
        )

        dev_frames[dev_indicator] = {
            "frame": create_development_dataframe(
                df_dev_raw,
                dev_config
            ),
            "description": (
                dev_config["indicators"][dev_indicator]
                ["short_description"]
            ),
            "category": dev_category_name
        }


    # -------------------------------------------------------
    # Bildungs-DataFrames vorberechnen
    # -------------------------------------------------------

    edu_frames = {}

    for edu_indicator in edu_indicators:

        edu_data = edu_config["indicators"][edu_indicator]

        valid_offsets = {}

        for entry in edu_data["education_years"]:

            if (
                entry["year"] is None
                or entry["records"] < min_available_countries
            ):
                continue

            change_offset = entry["change_offset"]
            lag_factor = entry["lag_factor"]

            if change_offset not in valid_offsets:
                valid_offsets[change_offset] = {}

            valid_offsets[change_offset][lag_factor] = {
                "year": entry["year"],
                "records": entry["records"]
            }


        # Kein ausreichender Datensatz vorhanden
        if not valid_offsets:
            continue


        df_edu_raw = create_indicator_frame(
            df_edu_origin,
            edu_indicator
        )

        edu_category = (
            edu_config["indicators"][edu_indicator]["category"]
        )

        edu_category_name = get_category_name(
            edu_config,
            edu_category
        )


        edu_frames[edu_indicator] = {
            "frame": create_education_dataframe(
                df_edu_raw,
                edu_config
            ),
            "description": edu_data["short_description"],
            "category": edu_category_name,
            "valid_offsets": valid_offsets
        }


    # -------------------------------------------------------
    # Alle Kombinationen berechnen
    # -------------------------------------------------------

    results = {}


    for dev_indicator, dev_info in dev_frames.items():

        df_dev = dev_info["frame"]

        dev_category = dev_info["category"]
        dev_description = dev_info["description"]


        for edu_indicator, edu_info in edu_frames.items():

            df_edu = edu_info["frame"]

            edu_category = edu_info["category"]
            edu_description = edu_info["description"]


            # Nur tatsächlich vorhandene Kombinationen nutzen
            for change_offset, lag_data in edu_info["valid_offsets"].items():

                for lag_factor in lag_data.keys():

                    df_analysis = merge_dev_edu_data(
                        df_dev,
                        df_edu,
                        change_offset,
                        lag_factor
                    )


                    if len(df_analysis) < min_available_countries:
                        continue


                    analysis_key = create_analysis_key(
                        dev_indicator,
                        edu_indicator,
                        change_offset,
                        lag_factor
                    )


                    results[analysis_key] = create_correlation_result(
                        development_indicator=dev_description,
                        education_indicator=edu_description,
                        development_category=dev_category,
                        education_category=edu_category,
                        change_offset=change_offset,
                        lag_factor=lag_factor,
                        analysis_df=df_analysis
                    )


    dump_json(
        CORRELATION_RESULTS,
        results
    )

main_function()