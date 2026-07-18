import pandas as pd
from pathlib import Path

from utils.hilfsfunktionen import create_frames
from src.preparations import load_config

from src.paths import DEVELOPMENT_CONFIG

EDU_INDICATOR = "timss_grade8_science"
DEV_INDICATOR = "gdp_per_capita"

EDU_INDICATOR_CODE = "LO.TIMSS.SCI8"
DEV_INDICATOR_CODE = "NY.GDP.PCAP.KD"

df_edu_wide, df_edu_long = create_frames(EDU_INDICATOR_CODE, "edu", "timss_science") 
df_dev_wide, df_dev_long = create_frames(DEV_INDICATOR_CODE, "dev", "gdp")


# ==========================================================================================
# Change Columns erzeugen
# ==========================================================================================

    # ======================================================================================
    # Change-relevante Informationen aus der Config-Datei importieren
    # ======================================================================================

def set_dev_change_data (config: dict, indicator: str) -> tuple[int, list[int], int, str]:
    if (not "meta_data" in config) or (not "indicators" in config):
        return None, None, None
    
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

def calc_growth (old, new) -> float:
    return (new - old) / old * 100

def calc_decrease_positive (old, new) -> float:
    return (old - new) / old * 100

def calc_difference (old, new) -> float:
    return new - old

# =======================================================================================
CHANGE_FUNCTIONS = {
    "growth": calc_growth,
    "decrease_positive": calc_decrease_positive,
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


# ========================================================================================
# Erzeugt Kandidatenjahre für einen Offset
# ========================================================================================

def get_candidate_years(target_year: int, tolerance: int) -> list[str]:
    """
    Erzeugt eine Liste möglicher Vergleichsjahre.
    
    Beispiel:
    target_year=2014, tolerance=2

    Ergebnis:
    ["2014", "2013", "2015", "2012", "2016"]
    """

    candidate_years = []

    for step in range(0, 2 * tolerance  + 1): 
        candidate_years.append(str(target_year + ((-1) ** step) * step))

    return candidate_years


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

    candidate_years = get_candidate_years(
        target_year,
        tolerance
    )

    for year in candidate_years:

        if (year in row.index) and (pd.notna(row[year])):
            return year

    return None


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
    """
    Berechnet alle Change-Werte für eine einzelne Datenzeile.
    """

    max_year_column = str(max_year)

    for offset in change_offsets:

        target_year = max_year - offset

        compare_year = find_comparison_year(row, target_year, offset_tolerance)

        column_name = f"change_over_{offset}_years"

        if compare_year:
            row[column_name] = change_type_calc(
                change_type,
                row[compare_year],
                row[max_year_column]
            )

        else:
            row[column_name] = None

    return row

# =============================================================================================================
# Finales Erzeugen der neuen Change-Value-Spalten
# =============================================================================================================

def create_dev_change_columns(df: pd.DataFrame, config_path: Path) -> pd.DataFrame:
    """
    Erzeugt für einen DataFrame im Wide-Format anhand von Offset-Werten eine neue Spalte pro Offset
    mit einem Delta oder Wachstumsrate innerhalb vergangener Zeiträume relativ zum aktuellsten Jahr. 
    """

    if df.empty:
        return df

    config = load_config(config_path)

    indicator = df["indicator_code"].iloc[0]

    max_year, change_offsets, offset_tolerance, change_type = set_dev_change_data(config, indicator)

    return df.apply(
        calculate_row_changes,
        axis=1,
        args=(
            max_year,
            change_offsets,
            offset_tolerance,
            change_type
        )
    )

