import pandas as pd
import json
from pathlib import Path
from utils.hilfsfunktionen import extract_year_columns, dump_json
from src.paths import (
    DEVELOPMENT_RAW,
    EDUCATION_RAW,
    PROCESSED_DATA_DIR,
    DEVELOPMENT_OUTPUT,
    EDUCATION_OUTPUT,
    DEVELOPMENT_CONFIG,
    EDUCATION_CONFIG,
    COUNTRY_INFO
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

def set_year_from_config (config) -> int:
    """
    Entnimmt der Konfigurations-Datei das hinterlegte max_year
    """

    meta_data = config["meta_data"]

    if not "max_year" in meta_data:
        return None
    else:
        return meta_data["max_year"]

# ================================================================================
# Reduktion von Jahresspalten auf die letzten "x" Jahre
# ================================================================================

def reduce_to_max_year (df: pd.DataFrame, max_year: int) -> pd.DataFrame:
    """
    Entfernt Jahresspalten aus dem DataFrame, 
    die über dem definierten max_year liegen
    """

    year_columns = extract_year_columns(df)

    years_not_over_max = [
        year 
        for year in year_columns
        if int(year) <= max_year
    ]

    return df[BASE_COLUMNS + years_not_over_max]


# ===============================================================================================
# Extrahieren der Ländercodes aller tatsächlichen Länder aus country_info
# zum Herausfiltern aller gruppierten Regionen
# ===============================================================================================

def extract_real_country_codes () -> list[str]:
    """
    Erzeugt eine Liste mit Ländercodes für ungruppierte Länder aus der country_info 
    """

    df_country_info = pd.read_csv(COUNTRY_INFO, encoding="utf-8")

    filter_real_countries = df_country_info["Region"].notna()

    df_real_country_info = df_country_info[filter_real_countries]

    return list(df_real_country_info["Country Code"].unique())

# ===============================================================================================
# Filtert einen DataFrame mit Spalte "Country Code" anhand einer Liste von country_codes
# ===============================================================================================

def filter_only_real_countries(df: pd.DataFrame, country_codes: list[str]) -> pd.DataFrame:
    """
    Filtert einen DataFrame mit Spalte "Country Code" anhand einer Liste von country_codes
    """

    if not "Country Code" in df.columns:
        return df

    filter = df["Country Code"].isin(country_codes)
    return df[filter]


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

    max_year = set_year_from_config(config)

    if max_year:
        df_filtered_indicators = reduce_to_max_year(df_filtered_indicators, max_year)

    years = get_available_year_columns(df_filtered_indicators)

    df_relevant_years = df_filtered_indicators[BASE_COLUMNS + years]

    country_codes = extract_real_country_codes()

    df_real_countries = filter_only_real_countries(df_relevant_years, country_codes)

    df_analysis = remove_empty_countries(df=df_real_countries, year_columns=years)

    output_path = create_output_path(output_directory, config)

    save_dataframe(df_analysis, output_path)


# ===============================================================================================
# ===============================================================================================
# Implementieren der Verfügbarkeit benötigter Bildungsjahrgänge pro Bildungsindikator
# ===============================================================================================
# ===============================================================================================

# ===============================================================================================
# Überprüft eine Liste von Jahren auf Verfügbarkeit eines Jahres innerhalb der Toleranz
# ===============================================================================================

def find_matching_year(
    available_years: list[int],
    target_year: int,
    tolerance: int
) -> int | None:
    """
    Liefert das nächstliegende vorhandene Jahr innerhalb der Toleranz.
    """

    candidate_years = []

    for step in range(0, 2 * tolerance  + 1): 
        candidate_years.append(target_year + ((-1) ** step) * step)
   
    for year in candidate_years:
        if year in available_years:
            return year

    return None


# ===============================================================================================
# Gibt eine Liste von im DataFrame verfügbaren Jahren für einen Bildungsindikator aus
# ===============================================================================================


def get_indicator_available_years(
    df: pd.DataFrame,
    indicator_code: str
) -> list[int]:
    """
    Liefert alle vorhandenen Jahre eines Bildungsindikators.
    """

    df_indicator = df[
        df["Indicator Code"] == indicator_code
    ]

    year_columns = get_available_year_columns(df_indicator)

    return [int(year) for year in year_columns]


# ===============================================================================================
# Implementiert final die verfügbaren Bildungsjahrgänge pro Indikator in die education_config
# ===============================================================================================

def update_education_years(config: dict) -> dict:
    """
    Implementiert die im aktuellen Datenstand verfügbaren Bildungsjahrgänge 
    pro Indikator in die education_config
    """

    meta = config["meta_data"]

    max_year = meta["max_year"]
    offsets = meta["change_offsets"]
    tolerance = meta["offset_tolerance"]

    df = pd.read_csv(EDUCATION_OUTPUT, encoding="utf-8")

    indicators = config["indicators"]

    for indicator_code, indicator_data in indicators.items():

        lag = indicator_data["recommended_lag"]

        available_years = get_indicator_available_years(df, indicator_code)

        education_years = {}

        for offset in offsets:
            target_year = max_year - offset - lag

            year = find_matching_year(
                available_years,
                target_year,
                tolerance
            )

            education_years[str(offset)] = year

        indicator_data["education_years"] = education_years

    return config



def update_categories(config: dict) -> dict:
    """
    Synchronisiert die Kategorienliste mit den aktuell vorhandenen Indikatoren.
    Neue Kategorien werden mit name=None angelegt.
    Nicht mehr verwendete Kategorien werden entfernt.
    """

    current_categories = config["meta_data"].get("categories", [])
    indicators = config["indicators"]

    new_category_list = []

    indicator_categories = {
        indicator["category"]
        for indicator in indicators.values()
        if "category" in indicator
    }

    for category in indicator_categories:
        existing_category = None

        for item in current_categories:
            if item["category"] == category:
                existing_category = item
                break

        if existing_category:
            new_category_list.append(existing_category)

        else:
            new_category_list.append(
                {
                    "category": category,
                    "name": None
                }
            )

    config["meta_data"]["categories"] = new_category_list

    return config



# ===============================================================================================
# Daten Update Funktion
# ===============================================================================================


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

    edu_config = load_config(EDUCATION_CONFIG)
    edu_config = update_education_years(edu_config)
    dump_json(EDUCATION_CONFIG, edu_config)
    
    dev_config = load_config(DEVELOPMENT_CONFIG)
    dev_config = update_categories(dev_config)
    dump_json(DEVELOPMENT_CONFIG, dev_config)
    
    

if __name__ == "__main__":

    update_data()