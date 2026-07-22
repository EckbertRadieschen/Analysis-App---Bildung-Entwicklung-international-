from pathlib import Path
import pandas as pd
import streamlit as st
import json
from utils.hilfsfunktionen import dump_json
from src.preparations import load_config
from scipy.stats import pearsonr, spearmanr

# =========================================================
# Erzeugt einen eindeutigen Dictionary Key 
# =========================================================

def create_analysis_key(
    development_indicator: str,
    education_indicator: str,
    change_offset: int
) -> str:

    return (
        f"{development_indicator}"
        f"__{education_indicator}"
        f"__{change_offset}"
    )


# =========================================================
# Lädt die eine JSON Datei, falls vorhanden
# =========================================================

def load_json_if_exists(path: Path) -> dict:
    """
    Lädt eine JSON-Datei, falls sie existiert.
    Gibt ansonsten ein leeres Dictionary zurück.
    """

    if not path.exists():
        return {}

    return load_config(path)


# =========================================================
# Gibt Korrelations-relevanten DataFrame aus
# =========================================================

def get_correlation_data(
    df: pd.DataFrame,
    change_offset: int
) -> pd.DataFrame:

    return (
        df[
            [
                f"value_education_year_{change_offset}",
                f"change_over_{change_offset}_years"
            ]
        ]
        .dropna()
    )


# =========================================================
# Berechnet die Pearson- und Spearman-Korrelation
# =========================================================

def calculate_correlations(
    df: pd.DataFrame,
    change_offset: int
) -> dict:

    correlation_df = get_correlation_data(df, change_offset)

    x = correlation_df[f"value_education_year_{change_offset}"]
    y = correlation_df[f"change_over_{change_offset}_years"]

    pearson_r, pearson_p = pearsonr(x, y)

    spearman_r, spearman_p = spearmanr(x, y)

    return {
        "n": len(correlation_df),

        "pearson_r": pearson_r,
        "pearson_p": pearson_p,

        "spearman_r": spearman_r,
        "spearman_p": spearman_p,
    }

# =========================================================
# Berechnet ggf. ein Korrelationsergebnis und gibt 
# für die aktuelle Kombination von Indikatoren
# das Korrelationsergebnis aus
# =========================================================

def get_or_create_correlation_result(
    correlation_result: dict,
    development_indicator: str,
    education_indicator: str,
    development_category: str,
    education_category: str,
    change_offset: int,
    analysis_df: pd.DataFrame,
    save_path: Path
) -> dict:
    """
    Prüft, ob eine Korrelationsanalyse bereits existiert.
    Falls nicht, wird sie berechnet, in das Dictionary aufgenommen
    und dauerhaft gespeichert.

    Gibt immer das Analyse-Ergebnis zurück.
    """

    correlation_results = st.session_state.get("correlation_results", {})
    correlation_results = {}

    analysis_key = create_analysis_key(development_indicator, education_indicator, change_offset)

    if correlation_results and (analysis_key in correlation_results):
        st.session_state["current_correlation_result"] = correlation_results[analysis_key]
        return correlation_results[analysis_key]

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

    correlation_results[analysis_key] = correlation_result

    dump_json(
        save_path,
        correlation_results
    )

    st.session_state["current_correlation_result"] = correlation_result

    return correlation_result