import pandas as pd
import numpy as np
from pathlib import Path
import streamlit as st
import plotly.express as px
from plotly.graph_objects import Figure

from utils.hilfsfunktionen import get_max_year_from_config, select_dataframe, find_relevant_years
from src.preparations import load_config

from src.paths import (
    DEVELOPMENT_CONFIG,
    DEVELOPMENT_OUTPUT,
    EDUCATION_CONFIG,
    EDUCATION_OUTPUT
)



# ==========================================================================================
# Change Columns erzeugen
# ==========================================================================================

    # ======================================================================================
    # Relevante Informationen aus der Development-Config-Datei importieren
    # ======================================================================================

def set_dev_change_data (config: dict, indicator: str) -> tuple[int, list[int], int, str]:
   
    meta_data = config["meta_data"]
    max_year = meta_data["max_year"]
    change_offsets = meta_data["change_offsets"]
    offset_tolerance = meta_data["offset_tolerance"]

    indicator_data = config["indicators"]
    values = indicator_data[indicator]
    change_type = values["change_type"]

    return max_year, change_offsets, offset_tolerance, change_type


# ======================================================================================
# Relevante Informationen aus der Education-Config-Datei importieren
# ======================================================================================

def set_edu_change_data(config: dict, indicator: str) -> tuple[int, list[int], int, int]:

    meta_data = config["meta_data"]

    max_year = meta_data["max_year"]
    change_offsets = meta_data["change_offsets"]
    offset_tolerance = meta_data["offset_tolerance"]

    indicator_data = config["indicators"]
    values = indicator_data[indicator]

    recommended_lag = values["recommended_lag"]

    return (
        max_year,
        change_offsets,
        offset_tolerance,
        recommended_lag,
    )

# ======================================================================================
# Change-Calc-Functions (3 verschiedene)
# ======================================================================================

def calc_growth (old, new) -> float | None:
    if old <= 0:
        return None
    
    return (new - old) / old * 100

def calc_difference (old, new) -> float:
    return new - old

# =======================================================================================
CHANGE_FUNCTIONS = {
    "growth": calc_growth,
    "difference": calc_difference,
}

# =======================================================================================
# Change-Typ-abhängiger Aufruf einer Change-Calc Funktion
# =======================================================================================

def change_type_calc (change_type: str, old_value: float, new_value: float) -> float:
    try: 
        change_function = CHANGE_FUNCTIONS[change_type]

    except KeyError:
        raise ValueError(f"Unknown change_type: {change_type}")

    return change_function(old_value, new_value)



# ================================================================================
# Findet verfügbares Vergleichsjahr innerhalb einer Zeile
# ================================================================================

def find_comparison_year(
    row: pd.Series,
    target_year: int,
    tolerance: int
) -> str | None:
    """
    Sucht innerhalb einer Zeile nach dem nächsten verfügbaren Vergleichsjahr.
    """

    candidate_years = []
    
    for step in range(0, 2 * tolerance  + 1): 
        candidate_years.append(str(target_year + ((-1) ** step) * step))

    for year in candidate_years:

        if (year in row.index) and (pd.notna(row[year])):
            return year

    return None


def find_available_max_year(
    row: pd.Series,
    max_year: int,
    tolerance: int
) -> int | None:
    """
    Sucht innerhalb einer Zeile nach dem nächsten verfügbaren Maximalen Jahr.
    """
   
    for step in range(0, tolerance + 1): 
        year = max_year - step
        year_col = str(year)

        if year_col in row.index and pd.notna(row[year_col]):
            return year

    return max_year


# ================================================================================
# Erzeugt Change-Werte für eine einzelne Zeile des Entwicklungs-DataFrames
# ================================================================================

def calculate_row_development_values(
    row: pd.Series,
    max_year: int,
    change_offsets: list[int],
    offset_tolerance: int,
    change_type: str
) -> pd.Series:
    """
    Erstellt für eine Datenzeile einen neuen Datensatz mit allen
    benötigten Entwicklungsänderungen.
    """

    available_max_year = find_available_max_year(
        row,
        max_year,
        offset_tolerance
    )

    result = {
        "country_name": row["country_name"],
        "country_code": row["country_code"],
        "dev_indicator_name": row["indicator_name"],
        "dev_indicator_code": row["indicator_code"],
        "available_max_year": available_max_year,
        "value_available_max_year": (
            row[str(available_max_year)]
            if available_max_year 
            else np.nan
        ),
    }

    for offset in change_offsets:

        target_year = available_max_year - offset

        comparison_year = find_comparison_year(
            row,
            target_year,
            offset_tolerance
        )

        result[f"available_comparison_year_{offset}"] = comparison_year

        if comparison_year is not None:

            old_value = row[comparison_year]
            new_value = row[str(available_max_year)]

            result[f"value_available_comparison_year_{offset}"] = old_value
            result[f"change_over_{offset}_years"] = change_type_calc(
                change_type,
                old_value,
                new_value
            )

        else:

            result[f"value_available_comparison_year_{offset}"] = np.nan
            result[f"change_over_{offset}_years"] = np.nan

    return pd.Series(result)


# ================================================================================
# Erzeugt Change-Werte für eine einzelne Zeile des Bildungs-DataFrames
# ================================================================================

def calculate_row_education_values(
    row: pd.Series,
    max_year: int,
    recommended_lag: int,
    change_offsets: list[int],
    offset_tolerance: int,
) -> pd.Series:
    """
    Erstellt für eine Bildungszeile einen neuen Datensatz mit den
    Bildungswerten zu den benötigten Vergleichsjahren.
    """

    result = {
        "country_name": row["country_name"],
        "country_code": row["country_code"],
        "edu_indicator_name": row["indicator_name"],
        "edu_indicator_code": row["indicator_code"],
    }

    for offset in change_offsets:

        lag = recommended_lag + offset

        target_year = max_year - lag

        education_year = find_comparison_year(
            row,
            target_year,
            offset_tolerance
        )

        result[f"education_year_{offset}"] = education_year

        if education_year is not None:
            result[f"value_education_year_{offset}"] = row[education_year]
        else:
            result[f"value_education_year_{offset}"] = np.nan

    return pd.Series(result)


# =============================================================================================================
# Finales Erzeugen des fertigen Entwicklungs-DataFrames
# =============================================================================================================

def create_development_dataframe(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Erzeugt für einen auf einen bestimmten Indikator gefilterten DataFrame im Wide-Format
    anhand von Offset-Werten eine neue Spalte pro Offset
    mit einem Delta oder einer Wachstumsrate innerhalb vergangener Zeiträume relativ zum aktuellsten Jahr. 
    """

    if df.empty:
        return df

    indicator = df["indicator_code"].iloc[0]

    max_year, change_offsets, offset_tolerance, change_type = set_dev_change_data(config, indicator)

    result = df.apply(
        calculate_row_development_values,
        axis=1,
        args=(
            max_year,
            change_offsets,
            offset_tolerance,
            change_type
        )
    )

    return result


# =============================================================================================================
# Finales Erzeugen des fertigen Bildungs-DataFrames
# =============================================================================================================

def create_education_dataframe(
    df: pd.DataFrame,
    config: dict
) -> pd.DataFrame:
    """
    Erstellt einen kompakten DataFrame mit den Bildungswerten
    der relevanten Jahre.
    """

    if df.empty:
        return df

    indicator = df["indicator_code"].iloc[0]

    max_year, change_offsets, offset_tolerance, recommended_lag = set_edu_change_data(config, indicator)

    result = df.apply(
        calculate_row_education_values,
        axis=1,
        args=(
            max_year,
            recommended_lag,
            change_offsets,
            offset_tolerance,
        )
    )

    return result


# =============================================================================================================
# Zusammenführen von Bildungs-Frame und Entwicklungs-Frame
# =============================================================================================================

def merge_dev_edu_data(
    df_dev: pd.DataFrame,
    df_edu: pd.DataFrame
) -> pd.DataFrame:
    """
    Führt Entwicklungs- und Bildungs-Daten anhand des Landes zusammen.
    """

    change_offset = st.session_state["selected_change_offset"]

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

# ================================================================================================================================
# Funktion zum Umwandeln in ein Wide- sowie ein Long-Format
# ================================================================================================================================

def create_indicator_frames (indicator_code: str, frame_name: str = "edu", indicator_title: str = "indicator") -> tuple[pd.DataFrame, pd.DataFrame]:
    """Bringt einen DataFrame in ein analysentaugliches Long-Format bzgl des vorgegebenen Indikators. 
    
        Args:
            indicator (str): Ein Indikator-Wert aus der Spalte 'Indicator Name' des Frames, nach dem gefiltert wird.
            frame_name (str, optional): 
                        Namens-Kürzel des DataFrames:
                            'edu': education_data (default)
                            'dev': development_data
            indicator_title (str, optional): Der Indikatorname, der für Benennungen verwendet werden soll. Defaults to "score".

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: Enthält zwei Versionen des df: gefiltert als Standardformat bzw. gefiltert als Long-Format
    """

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

    df_indicator = df_indicator[relevant_columns]

    df_indicator.sort_values([f"{indicator_title}_data_count", "country_name"], ascending=[False, True])

    df_indicator_long = df_indicator.melt(
        id_vars=["country_name", "country_code", "indicator_name", "indicator_code"],
        value_vars=years,
        var_name="year",
        value_name=f"{indicator_title}_score"
    )

    df_indicator_long["year"] = df_indicator_long["year"].astype(int)

    df_indicator_long = df_indicator_long.dropna(subset=[f"{indicator_title}_score"])

    df_indicator_long

    return df_indicator, df_indicator_long


# ==============================================================================================
# Import der vom User ausgewählten Indikatoren und change_offset
# ==============================================================================================

def get_analysis_data ():
    dev_indicator_dict = st.session_state.get("selected_development_indicator", None)
    dev_indicator = dev_indicator_dict["key"] if dev_indicator_dict else None

    edu_indicator_dict = st.session_state.get("selected_education_indicator", None)
    edu_indicator = edu_indicator_dict["key"] if edu_indicator_dict else None

    change_offset = st.session_state.get("selected_change_offset", None)

    return dev_indicator, edu_indicator, change_offset


# ==============================================================================================
# Export der Analyse-Frames in den session_state
# ==============================================================================================

def create_analysis_frames (dev_indicator: str, edu_indicator: str, dev_config: dict, edu_config: dict):
    dev_indicator, edu_indicator, change_offset = get_analysis_data()

    if not st.session_state.get("are_all_sidebar_selectors", False):
        return 

    df_dev_raw = create_indicator_frames(dev_indicator, "dev")[0]
    df_edu_raw = create_indicator_frames(edu_indicator, "edu")[0]

    df_dev = create_development_dataframe(df_dev_raw, dev_config)
    df_edu = create_education_dataframe(df_edu_raw, edu_config)
    
    st.session_state["development_frame"] = df_dev
    st.session_state["education_frame"] = df_edu
    st.session_state["comparison_frame"] = merge_dev_edu_data(df_dev, df_edu)

