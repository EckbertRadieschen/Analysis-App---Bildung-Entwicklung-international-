import pandas as pd
import numpy as np
import json
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from tabulate import tabulate
from src.paths import (
    EDUCATION_OUTPUT,
    DEVELOPMENT_OUTPUT
)

# =================================================================================================
# Funktionen zur ersten Übersicht bzgl Datenstruktur und -qualität
# =================================================================================================

def quality_frame (df: pd.DataFrame):
    datenqualitaet = pd.DataFrame({
        "Datentyp": df.dtypes,
        "Fehlende Werte": ((df.isnull().sum() / df.shape[0]) * 100).round(2),
        "Eindeutige Werte": df.nunique()
    })
    print(datenqualitaet)
    

def structure_frame (df: pd.DataFrame):
    zeilen = df.shape[0]

    spalten = df.shape[1]
    numerische_spalten = df.select_dtypes("number").shape[1]
    datums_spalten = df.select_dtypes("datetime").shape[1]
    object_spalten = df.select_dtypes("object").shape[1]
    category_spalten = df.select_dtypes("category").shape[1]

    duplikate = df.duplicated().sum()

    print(f"\nAnzahl Zeilen: {zeilen}\ndavon: {duplikate} Duplikate")
    print(f"\nAnzahl Spalten: {spalten}\ndavon:")
    print(f"    {numerische_spalten} numerisch")
    print(f"    {datums_spalten} datetime")
    print(f"    {object_spalten} string/object")
    print(f"    {category_spalten} kategorial\n")



def short_analysis_frame (df: pd.DataFrame):
    print("\n========== DataFrame Qualität ==========\n")
    structure_frame(df)
    quality_frame(df)


# =================================================================================================
# Value Counts Funktion
# =================================================================================================

def get_numeric_plot_type(values):

    unique = values.nunique()
    boundary = max(int(len(values) * 0.01), 100)

    if unique <= 20:
        return "bar"

    elif unique <= boundary:
        return "histogram"

    else:
        return "binned"

# ====================================================
def create_numeric_bins(values):
    max_value = values.max()
    min_value = values.min()

    if min_value == max_value:
        return [min_value, min_value + 1]

    q1 = values.quantile(0.25)
    q3 = values.quantile(0.75)

    iqr = q3 - q1

    upper_bound = q3 + 1.5 * iqr
    lower_bound = q1 - 1.5 * iqr

    is_lower_outlier = min_value < lower_bound
    is_upper_outlier = max_value > upper_bound

    bin_min = lower_bound if is_lower_outlier else min_value
    bin_max = upper_bound if is_upper_outlier else max_value
    
    normal_bins = 10
    if is_lower_outlier:
        normal_bins -= 1
    if is_upper_outlier:
        normal_bins -= 1

    bins = list(
        np.linspace(
            bin_min, 
            bin_max, 
            normal_bins + 1
        )
    )

    outer_bin_shift = (bins[-1] - bins[-2]) * 0.01
    
    if is_upper_outlier:
        bins.append(max_value + outer_bin_shift)
    else: 
        bins[-1] = bins[-1] + outer_bin_shift
    
    if is_lower_outlier:
        bins.insert(0, min_value)

    return bins

# ====================================================
def get_decimal_places(value):
    text = f"{value:.10f}".rstrip("0")
    
    if "." in text:
        return len(text.split(".")[1])
    
    return 0

# ====================================================
def create_bin_labels(bins, is_integer):
    if is_integer:
        decimals = 0
    else:
        bin_width = bins[1] - bins[0]
        decimals = get_decimal_places(bin_width)

    labels = []

    for left, right in zip(bins[:-1], bins[1:]):
        labels.append(
            f"{left:.{decimals}f} - {right:.{decimals}f}"
        )

    return labels

# ========================================================================
def apply_bins(values, bins, labels):
    binned_values = pd.cut(
        values,
        bins=bins,
        labels=labels,
        right=False
    )

    return binned_values

# ========================================================================
def all_numeric_counts (df: pd.DataFrame):
    numeric_columns = df.select_dtypes("number").columns

    value_count_figures = {}

    for column in numeric_columns:
        values = df[column].dropna()

        plot_type = get_numeric_plot_type(values)

        if plot_type == "bar":
            df_bar = values.value_counts().reset_index()
            df_bar.columns = [column, "Häufigkeit"]

            fig = px.bar(
                df_bar.sort_values(column),
                x=column,
                y="Häufigkeit",
                orientation="v",
                title = f"Verteilung der Werte in Spalte '{column}'"
            )
        elif plot_type == "histogram":
            fig = px.histogram(
                df,
                x=column,
                labels={
                    "count": "Häufigkeit"
                },
                title=f"Verteilung der Werte in Spalte '{column}'"
            )
            fig.update_layout(
                bargap=0.1
            )

        elif plot_type == "binned":            
            
            is_integer = np.isclose(values % 1, 0).all()

            bins = create_numeric_bins(values)

            labels = create_bin_labels(
                bins,
                is_integer
            )

            binned_values = apply_bins(
                values,
                bins,
                labels
            )

            value_counts = (
                binned_values
                .value_counts(sort=False)
                .reset_index()
            )

            value_counts.columns = [
                "Wertebereich",
                "Häufigkeit"
            ]

            fig = px.bar(
                value_counts,
                x="Wertebereich",
                y="Häufigkeit",
                title=f"Verteilung der Werte in Spalte '{column}'"
            )

        value_count_figures[column] = fig

    return value_count_figures


# ================================================================================================================================
# Funktion zur Ausgabe des gewünschten DataFrames anhand eine Namens-Kürzels
# ================================================================================================================================

def select_dataframe (frame_name: str = "edu") -> pd.DataFrame:
    """Erzeugt aus einem DataFrame-Namens-Kürzel den zugehörigen DataFrame

    Args: 
        frame_name (str, optional): 
            Namens-Kürzel des DataFrames:
                'edu': education_data (default)
                'dev': development_data

    Returns:
        pd.DataFrame: Aus der relevanten csv-Datei erzeugter DataFrame.
    """

    frame_names = ["edu", "dev"]
    if not frame_name in frame_names:
        return None

    if frame_name.lower() == "edu":
        df = pd.read_csv(EDUCATION_OUTPUT)
    if frame_name.lower() == "dev":
        df = pd.read_csv(DEVELOPMENT_OUTPUT)

    return df

# ================================================================================================================================
# Funktion zur Ausgabe nicht-leerer Integer-Titel-Spalten (Jahresspalten) eines DataFrames
# ================================================================================================================================

def find_relevant_years(df: pd.DataFrame) -> list[str]:
    """Reduziert Spalten, deren Titel eine Integer ist, auf diejenigen, die Werte enthalten."""

    col_list = df.columns
    
    year_cols = []

    for col in col_list:
        if col.isdigit():
            year_cols.append(col)

    relevant_years = [
        year 
        for year in year_cols
        if df[year].notna().any()
    ]
    
    for year in year_cols[-4:]:
        if not year in relevant_years:
            relevant_years.append(year)


    return relevant_years



def extract_year_columns(df: pd.DataFrame) -> list[str]:
    return [
            col 
            for col in df.columns 
            if col.isdigit()
        ]




def get_max_year_from_config(config: dict) -> int:
    """
    Entnimmt der Config den Meta-Wert "max_year" und gibt ihn als Zahl aus 
    """

    return int(config["meta_data"]["max_year"])


# ==================================================================
# JSON Dump
# ==================================================================

def json_serializer(obj):

    if isinstance(obj, np.integer):
        return int(obj)

    if isinstance(obj, np.floating):
        return float(obj)

    if isinstance(obj, np.ndarray):
        return obj.tolist()

    raise TypeError(
        f"Object of type {type(obj)} is not JSON serializable"
    )


def dump_json (save_path: Path, json_data: dict) -> None:
    with open(save_path, "w", encoding="utf-8") as file:
        json.dump(
            json_data,
            file,
            indent=4,
            ensure_ascii=False,
            default=json_serializer
        )


def drop_incomplete_records(df: pd.DataFrame):
    year_columns = extract_year_columns(df)
    