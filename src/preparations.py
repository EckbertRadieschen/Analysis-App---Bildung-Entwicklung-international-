import pandas as pd
import json
from pathlib import Path
from utils.hilfsfunktionen import extract_year_columns
from src.paths import (
    DEVELOPMENT_RAW,
    EDUCATION_RAW,
    DEVELOPMENT_CONFIG,
    EDUCATION_CONFIG,
    PROCESSED_DATA_DIR,
)

BASE_COLUMNS = [
        "Country Name",
        "Country Code",
        "Indicator Name",
        "Indicator Code"
    ]

# ================================================================================
# Rohdaten in DataFrame laden
# ================================================================================

def load_data(data_path: Path) -> pd.DataFrame:
    """
    Lädt eine Rohdaten-CSV in einen DataFrame
    """

    return pd.read_csv(data_path, encoding="utf-8")


# ================================================================================
# Konfigurationen laden
# ================================================================================

def load_config(config_path: Path) -> dict:
    """
    Lädt eine Konfigurations-Datei.
    """

    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)
    

# ================================================================================
# Speicherpfad erzeugen
# ================================================================================

def create_output_path (output_directory: Path, config: dict) -> Path:
    """
    Erzeugt aus einem Ziel-Directory und der Konfigurations-Datei einen Zielpfad
    """
    output_directory.mkdir(parents=True, exist_ok=True)

    file_name = config["meta_data"]["output_file_name"]

    return output_directory / file_name

# ================================================================================
# Rohdaten mithilfe einer Indikator-Konfiguration filtern
# ================================================================================

def filter_indicators(df_raw: pd.DataFrame, indicator_data: dict) -> pd.DataFrame:
    """
    Filtert Rohdaten auf die in der Config definierten Indikatoren.
    """

    indicator_codes = list(indicator_data.keys())

    return df_raw[
        df_raw["Indicator Code"].isin(indicator_codes)
    ]


# ================================================================================
# Erzeuge Liste mit Indikator-relevanten Jahren
# ================================================================================

def get_available_year_columns(df: pd.DataFrame) -> list[str]:
    """
    Gibt vorhandene und nicht vollständig leere Jahres-Spalten zurück.
    """

    year_columns = [
        col 
        for col in df.columns 
        if col.isdigit()
    ]

    relevant_years = [
        year 
        for year in year_columns
        if df[year].notna().sum() > 0
    ]

    return relevant_years


# ================================================================================
# Filtern auf Indikator- und Zeitraum-relevante Länder
# ================================================================================

def remove_empty_countries(df: pd.DataFrame, year_columns: list[str]) -> pd.DataFrame:
    """
    Entfernt Länder ohne jegliche Werte in den Jahres-Spalten.
    """

    return df[~df[year_columns].isna().all(axis=1)]


def save_dataframe(df: pd.DataFrame, output_path: Path) -> None:
    """
    Speichert einen DataFrame als CSV.
    """

    df.to_csv(
        output_path,
        index=False,
        encoding="utf-8"
    )

# ================================================================================
# Import der analyse-relevanten Jahresdaten aus Development-Configuration
# ================================================================================

def set_year_from_config (config) -> tuple[int, int]:
    """
    Entnimmt der Konfigurartions-Datei  
    """

    meta_data = config["meta_data"]

    if (not "max_year" in meta_data) or (not "years_offset" in meta_data):
        return None, None
    else:
        return meta_data["max_year"], meta_data["years_offset"]

# ================================================================================
# Reduktion von Jahresspalten auf die letzten "x" Jahre
# ================================================================================

def reduce_max_x_years_ago(df: pd.DataFrame, max_year: int, years_offset: int) -> pd.DataFrame:
    """
    Entfernt Jahresspalten aus dem DataFrame, 
    die länger als x Jahre in der Vergangenheit liegen
    """

    year_columns = extract_year_columns(df)

    years_in_offset = [
        year 
        for year in year_columns
        if (int(year) >= max_year - years_offset) and (int(year) <= max_year)
    ]

    return df[BASE_COLUMNS + years_in_offset]


# ===============================================================================================
# Erzeugen einer analyse-tauglichen CSV-Datei aus Rohdaten mithilfe 
# einer Konfigurationsdatei
# ===============================================================================================

def create_analysis_file(data_path: Path, config_path: Path, output_directory: Path) -> None:
    """
    Erstellt aus Rohdaten und einer Konfigurationsdatei
    eine analysefähige CSV-Datei.
    """

    df_raw = load_data(data_path)

    config = load_config(config_path)
    indicator_data = config["indicators"]

    df_filtered_indicators = filter_indicators(df_raw, indicator_data)

    max_year, years_offset = set_year_from_config(config)

    if max_year and years_offset:
        df_filtered_indicators = reduce_max_x_years_ago(df_filtered_indicators, max_year, years_offset)

    years = get_available_year_columns(df_filtered_indicators)

    df_analysis = df_filtered_indicators[BASE_COLUMNS + years]

    df_analysis = remove_empty_countries(df=df_analysis, year_columns=years)

    output_path = create_output_path(output_directory, config)

    save_dataframe(df_analysis, output_path)


def update_data():
    create_analysis_file(
        DEVELOPMENT_RAW,
        DEVELOPMENT_CONFIG,
        PROCESSED_DATA_DIR
    )

    create_analysis_file(
        EDUCATION_RAW,
        EDUCATION_CONFIG,
        PROCESSED_DATA_DIR
    )


if __name__ == "__main__":

    update_data()