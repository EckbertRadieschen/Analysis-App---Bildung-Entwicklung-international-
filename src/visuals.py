import pandas as pd
import streamlit as st
import re
import plotly.express as px
from plotly.graph_objects import Figure

from src.analysis import get_analysis_data
from src.preparations import load_config

from src.paths import DEVELOPMENT_CONFIG, EDUCATION_CONFIG


def format_value(value):
    bar_source_choice = st.session_state.get("main_bar_source_choice", "Entwicklungsvariable")

    value_formatted = str(round(value, 3)).replace(".", ",")

    signs = ["", ""] if bar_source_choice == "Bildungsindikator" else ["+", "+/- "]

    if round(value, 3) > 0:
        return f"{signs[0]}{value_formatted}"
    elif round(value, 3) < 0:
        return value_formatted
    else:
        return f"{signs[1]}{value_formatted}"


# ======================================================================================================================
# Top 10 Bar Chart
# ======================================================================================================================

def create_top_bottom_10_bar_chart(df: pd.DataFrame, change_offset: int, lag_factor: int) -> tuple[Figure, bool]:

    x_column = (
        f"change_over_{str(change_offset)}_years" 
        if f"change_over_{str(change_offset)}_years" in df.columns
        else f"value_education_year_{change_offset}_factor_{lag_factor}"
    )

    df = df[df[x_column].notna()]

    top_bottom_choice = st.session_state.get("top_bottom_choice", "Top 10")

    if top_bottom_choice == "Bottom 10":
        df = df.sort_values(x_column, ascending=True).head(10)
    elif top_bottom_choice == "Top 10":
        df = df.sort_values(x_column, ascending=True).tail(10)

    fig = px.bar(
        df.assign(label=lambda row: row[x_column].apply(format_value)),
        x=x_column,
        y="country_name",
        orientation="h",
        text="label" 
    )

    value_checker = (df[x_column] < 0).any() and (df[x_column] > 0).any()

    return fig, value_checker


# ======================================================================================================================
# Bar Chart Layout
# ======================================================================================================================

def set_bar_layouts (fig: Figure, config: dict, indicator_code: str) -> Figure:

    indicator_values = config["indicators"][indicator_code]
    indicator_short_description = indicator_values["short_description"]
    change_type = indicator_values.get("change_type", None)

    top_bottom = st.session_state.get("top_bottom_choice", "Top 10").title()
    main_bar_source_choice = st.session_state.get("main_bar_source_choice", "Entwicklungsvariable")

    match = re.search(r"\((.*?)\)", indicator_short_description)

    if match:
        indicator_unit = match.group(1)

    if main_bar_source_choice == "Entwicklungsvariable":
        x_axis_extension = (
            f" - Absolute Veränderung ({indicator_unit})" 
            if change_type == "difference"
            else " - Veränderung (%)"
        )

        x_title = indicator_short_description.split("(")[0] + x_axis_extension
        chart_title = f"{top_bottom} - Länder bzgl. Indikator-Trend im Vergleichszeitraum"

    elif main_bar_source_choice == "Bildungsindikator":
        x_title = indicator_short_description
        chart_title = f"{top_bottom} - Länder bzgl. Indikatorwert im relevanten Bildungsjahr"

    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title=None,
        title=chart_title,
        title_x=0.5,
        title_xanchor="center"
    )

    fig.update_xaxes(showticklabels=False)

    return fig


# ===========================================================================================
# Indikator Bar-Chart erzeugen
# ===========================================================================================

def create_indicator_bar_chart() -> Figure | None:

    dev_indicator_dict, edu_indicator_dict, change_offset, lag_factor = get_analysis_data()

    dev_indicator = dev_indicator_dict["key"]
    edu_indicator = edu_indicator_dict["key"]

    df_dev = st.session_state["development_frame"]
    df_edu = st.session_state["education_frame"]

    
    source = st.session_state.get("main_bar_source_choice", "Entwicklungsvariable")

    if source == "Entwicklungsvariable":
        indicator_code = dev_indicator
        df = df_dev
        config = load_config(DEVELOPMENT_CONFIG)
    elif source == "Bildungsindikator":
        indicator_code = edu_indicator
        df = df_edu
        config = load_config(EDUCATION_CONFIG)
    else:
        return None

    fig, value_checker = create_top_bottom_10_bar_chart(df, change_offset, lag_factor)

    fig.update_traces(
        marker_color="#e49650"
    )

    fig = set_bar_layouts(fig, config, indicator_code)

    if value_checker:

        fig.add_vline(
            x=0,
            line_width=1,
            line_color="gray"
        )

    return fig


# ===========================================================================================
# Zusammenhangs-Scatterplot erstellen
# ===========================================================================================

def create_education_development_scatterplot():
    """
    Erstellt einen Scatterplot zwischen Bildungswert und
    Entwicklungsveränderung für den gewählten Zeitraum.

    x-Achse: Bildungswert im historischen Jahr

    y-Achse: Veränderung des Entwicklungsindikators über den Zeitraum
    """

    df = st.session_state["comparison_frame"]
    dev_indicator_dict, edu_indicator_dict, change_offset, lag_factor = get_analysis_data()

    dev_indicator_description = dev_indicator_dict["name"]
    edu_indicator_description = edu_indicator_dict["name"]

    dev_x_axis_parts = dev_indicator_description.split("(")

    dev_x_axis = f"{dev_x_axis_parts[0]} - Veränderung ({dev_x_axis_parts[1]}"

    education_year = round(
        pd.to_numeric(
            df[f"education_year_{change_offset}_factor_{lag_factor}"],
            errors="coerce"
        ).mean()
    )

    education_column = f"value_education_year_{change_offset}_factor_{lag_factor}"
    development_column = f"change_over_{change_offset}_years"

    fig = px.scatter(
        df,
        x=education_column,
        y=development_column,
        hover_name="country_name",
        title=(
            f"Für Vergleichszeitraum {change_offset} Jahre"
            f" und Bildungsjahr {education_year}"
        ),
        labels={
            education_column: edu_indicator_description,
            development_column: dev_indicator_description
        },
        trendline="ols"
    )

    fig.update_layout(
        xaxis_title=edu_indicator_description,
        yaxis_title=dev_x_axis,
        title_x=0.5,
        title_xanchor="center"
    )

    fig.update_traces(
        marker_color="#e49650"
    )

    return fig

# ===========================================================================================
# Zusammenhangs-Scatterplot erstellen
# ===========================================================================================

def choose_main_chart ():
    source = st.session_state.get("main_bar_source_choice", "Entwicklungsvariable")
    if source == "Zusammenhang":
        return create_education_development_scatterplot()
    elif source in ["Entwicklungsvariable", "Bildungsindikator"]:
        return create_indicator_bar_chart()
    else: 
        return None