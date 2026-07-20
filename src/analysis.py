import pandas as pd
import numpy as np
from pathlib import Path
import streamlit as st
import plotly.express as px
from plotly.graph_objects import Figure

from utils.hilfsfunktionen import get_max_year_from_config, select_dataframe, find_relevant_years
from src.preparations import load_config

from src.paths import DEVELOPMENT_CONFIG



# ==========================================================================================
# Change Columns erzeugen
# ==========================================================================================

    # ======================================================================================
    # Change-relevante Informationen aus der Config-Datei importieren
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
# Erzeugt Change-Werte für eine einzelne Zeile
# ================================================================================

def calculate_row_changes(
    row: pd.Series,
    max_year: int,
    change_offsets: list[int],
    offset_tolerance: int,
    change_type: str
) -> pd.Series:
    """Berechnet alle Change-Werte für eine einzelne Datenzeile"""

    available_max_year = find_available_max_year(row, max_year, 2)

    for offset in change_offsets:

        target_year = available_max_year - offset
        
        compare_year = find_comparison_year(row, target_year, offset_tolerance)

        column_name = f"change_over_{offset}_years"

        if compare_year:
            row[column_name] = change_type_calc(
                change_type,
                row[compare_year],
                row[str(available_max_year)]
            )

        else:
            row[column_name] = np.nan

    return row

# =============================================================================================================
# Finales Erzeugen der neuen Change-Value-Spalten
# =============================================================================================================

def create_dev_change_columns(df: pd.DataFrame, config: dict) -> pd.DataFrame:
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
        calculate_row_changes,
        axis=1,
        args=(
            max_year,
            change_offsets,
            offset_tolerance,
            change_type
        )
    )

    return result


# ================================================================================================================================
# Funktion zum Umwandeln in ein Long-Format
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


def get_analysis_data ():
    dev_indicator_tuple = st.session_state.get("selected_development_indicator", None)
    dev_indicator = dev_indicator_tuple[0] if dev_indicator_tuple else None

    edu_indicator_tuple = st.session_state.get("selected_education_indicator", None)
    edu_indicator = edu_indicator_tuple[0] if edu_indicator_tuple else None

    change_offset = st.session_state.get("selected_change_offset", None)

    return dev_indicator, edu_indicator, change_offset


def create_analysis_frames (dev_config: dict):
    dev_indicator, edu_indicator, change_offset = get_analysis_data()

    if not st.session_state.get("are_all_sidebar_selectors", False):
        return 

    dev_frame_wide, dev_frame_long = create_indicator_frames(dev_indicator, frame_name="dev")
    edu_frame_wide, edu_frame_long = create_indicator_frames(edu_indicator, frame_name="edu")

    dev_frame_wide = create_dev_change_columns(dev_frame_wide, dev_config)

    st.session_state["development_frames"] = [dev_frame_wide, dev_frame_long]
    st.session_state["education_frames"] = [edu_frame_wide, edu_frame_long]


