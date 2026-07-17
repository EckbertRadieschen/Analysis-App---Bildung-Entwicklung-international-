import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from tabulate import tabulate
from src.paths import (
    EDUCATION_OUTPUT,
    DEVELOPMENT_OUTPUT
)
from src.preparations import filter_indicators

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

    year_cols_relevant = []

    for col in year_cols:
        values_count = df[col].notna().sum()
        if values_count > 0:
            year_cols_relevant.append(col)

    return year_cols_relevant

# ================================================================================================================================
# Funktion zum Umwandeln in ein Long-Format
# ================================================================================================================================

def create_frames (indicator_code: str, frame_name: str = "edu", indicator_title: str = "indicator") -> tuple[pd.DataFrame, pd.DataFrame]:
    """Bringt einen DataFrame in ein analysentaugliches Long-Format bzgl des vorgegebenen Indikators. 
    
        Args:
            indicator (str): Ein Indikator-Wert aus der Spalte 'Indicator Name' des Frames, nach dem gefiltert wird.
            frame_name (str, optional): 
                        Namens-Kürzel des DataFrames:
                            'edu': education_data (default)
            indicator_title (str, optional): Der Indikatorname, der für Benennungen verwendet werden soll. Defaults to "score".

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: Enthält zwei Versionen des df: gefiltert als Standardformat bzw. gefiltert als Long-Format
    """

    df = select_dataframe(frame_name)

    df_indicator = df[df["Indicator Code"] == indicator_code]

    years = find_relevant_years(df_indicator)

    df_indicator[f"{indicator_title}_data_count"] = df_indicator[years].notna().sum(axis=1)

    df_indicator = df_indicator[
        df_indicator[f"{indicator_title}_data_count"] > 0
    ]

    relevant_columns = [
        'Country Name',
        'Country Code',
        'Indicator Name',
        'Indicator Code',
        f'{indicator_title}_data_count'
    ] + years

    df_indicator = df_indicator[relevant_columns]

    df_indicator.columns = (
        df_indicator.columns
        .str.lower()
        .str.replace(" ", "_")
    )

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


def extract_year_columns(df: pd.DataFrame) -> list[str]:
    return [
            col 
            for col in df.columns 
            if col.isdigit()
        ]


def drop_incomplete_records(df: pd.DataFrame):
    year_columns = extract_year_columns(df)
    