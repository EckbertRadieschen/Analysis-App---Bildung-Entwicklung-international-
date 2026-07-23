import pandas as pd
import streamlit as st

from app.statistics_sidebar import statistics_sidebar_content


def load_category_statistics() -> None:
    """
    Erstellt einen DataFrame mit Kennzahlen pro Bildungs- und
    Entwicklungskategorie und speichert ihn im Session State.
    """

    df = st.session_state["correlation_results_dataframe"]

    rows = []

    for category_type in ["development", "education"]:

        category_column = f"{category_type}_category"

        for category, group in df.groupby(category_column):

            rows.append({
                "category_type": category_type,
                "category": category,

                "count": len(group),

                "median_abs_r": group["pearson_r"].abs().median(),
                "mean_abs_r": group["pearson_r"].abs().mean(),

                "significant_count": (group["pearson_p"] < 0.05).sum(),
                "strong_count": (group["pearson_r"].abs() >= 0.5).sum()
            })

    st.session_state["category_statistics"] = pd.DataFrame(rows)



def statistic_page():
    statistics_sidebar_content()