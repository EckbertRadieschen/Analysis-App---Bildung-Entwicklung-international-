import pandas as pd
import streamlit as st
import re
import plotly.express as px
from plotly.graph_objects import Figure

from src.analysis import get_analysis_data
from src.preparations import load_config

from src.paths import DEVELOPMENT_CONFIG, EDUCATION_CONFIG


def format_value(value):
    if round(value, 3) > 0:
        return (f"+{round(value, 3)}").replace(".", ",")
    elif round(value, 3) < 0:
        return (f"{round(value, 3)}").replace(".", ",")
    else:
        return "+/- 0"


# ======================================================================================================================
# Top 10 Bar Chart
# ======================================================================================================================

def create_top_bottom_10_bar_chart(df: pd.DataFrame, change_offset: int) -> tuple[Figure, bool]:

    x_column = f"change_over_{str(change_offset)}_years"

    df = df[df[x_column].notna()]

    top_bottom_choice = st.session_state.get("top_bottom_choice", "top")

    if top_bottom_choice == "bottom":
        df = df.sort_values(x_column, ascending=True).head(10)
    elif top_bottom_choice == "top":
        df = df.sort_values(x_column, ascending=True).tail(10)

    fig = px.bar(
        df.assign(
            label=lambda row: row[x_column].apply(format_value)
        ),
        x=x_column,
        y="country_name",
        orientation="h",
        text="label"
    )

    value_checker = (df[x_column] < 0).any() and (df[x_column] > 0).any()

    return fig, value_checker


def set_bar_layouts (fig: Figure, config: dict, indicator_code: str) -> Figure:

    indicator_values = config["indicators"][indicator_code]
    indicator_short_description = indicator_values["short_description"]
    change_type = indicator_values.get("change_type", None)

    top_bottom = st.session_state.get("top_bottom_choice", "top").title()
    main_bar_source_choice = st.session_state.get("main_bar_source_choice", "development")

    match = re.search(r"\((.*?)\)", indicator_short_description)

    if match:
        indicator_unit = match.group(1)

    if main_bar_source_choice == "development":
        x_axis_extension = (
            f" - Absolute Veränderung ({indicator_unit})" 
            if change_type == "difference"
            else " - Veränderung (%)"
        )

        x_title = indicator_short_description.split("(")[0] + x_axis_extension

    elif main_bar_source_choice == "education":
        pass

    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title=None,
        title=f"{top_bottom} 10 - Länder bzgl. Indikator"
    )

    fig.update_xaxes(showticklabels=False)

    return fig

# ===========================================================================================
# Indikator Bar-Chart erzeugen
# ===========================================================================================

def create_indicator_bar_chart() -> Figure | None:

    dev_indicator, edu_indicator, change_offset = get_analysis_data()

    df_dev = st.session_state["development_frames"][0]
    df_edu = st.session_state["education_frames"][0]

    source = st.session_state.get("main_bar_source_choice", "development")

    if source == "development":
        indicator_code = dev_indicator
        df = df_dev
        config = load_config(DEVELOPMENT_CONFIG)
    elif source == "education":
        indicator_code = edu_indicator
        df = df_edu
        config = load_config(EDUCATION_CONFIG)
    else:
        return None

    fig, value_checker = create_top_bottom_10_bar_chart(df, change_offset)

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