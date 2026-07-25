import pandas as pd
import numpy as np
import streamlit as st
import re
import plotly.express as px
import plotly.graph_objects as go
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


# ===========================================================================================
# Bar-Chart Korrelationen alle Kategorien
# ===========================================================================================

def create_category_statistics_bar_chart(
    category_type: str,
    evaluation: dict,
    strictness: dict
):
    """
    Erstellt ein Balkendiagramm für Kategorie-Statistiken.

    category_type: "development" oder "education"

    evaluation: Dictionary mit label und value_column
    """

    df = st.session_state["category_statistics"].copy()

    df = df[df["category_type"] == category_type]

    value_column = evaluation["value_column"]
    evaluation_type = evaluation["label"]
    threshold = strictness["value"]
    

    df = df.sort_values(value_column,ascending=True)

    chart_title = (
        "Entwicklung" 
        if category_type == "development"
        else "Bildung"
    )

    fig = px.bar(
        df,
        x=value_column,
        y="category",
        orientation="h",
        text=value_column
    )

    max_value = df[value_column].max()
    x_scale_upper = np.ceil(max_value * 1.01 * 10) / 10

    fig.update_xaxes(visible=False)
    if evaluation_type == "Durchschnittliche Zusammenhangsstärke":
        fig.update_xaxes(range=[threshold, x_scale_upper])

    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        height=220,
        margin=dict(
            l=160,
            r=20,
            t=35,
            b=5
        ),
        title=dict(
            text=chart_title,
            x=0.5,
            xanchor="center",
            font=dict(size=14)
        )
    )

    fig.update_traces(
        marker_color="#e49650",
        textfont=dict(size=10)
    )

    if value_column == "relevance_ratio":
        fig.update_traces(
            texttemplate="%{text:.1%}"
        )
    else:
        fig.update_traces(
            texttemplate="%{text:.2f}"
        )

    if value_column == "relevance_ratio":
        hovertemplate = (
            "<b>%{y}</b><br><br>"
            "Relevante Zusammenhänge: "
            "<b>%{customdata[0]}</b> von "
            "<b>%{customdata[1]}</b><br>"
            "Trefferquote: "
            "<b>%{x:.1%}</b>"
            "<extra></extra>"
        )

        customdata = df[["count", "total_count"]].values


    elif value_column == "sum_abs_r":
        hovertemplate = (
            "<b>%{y}</b><br><br>"
            "Kumulierte Zusammenhangsstärke: "
            "<b>%{x:.2f}</b><br>"
            "Relevante Zusammenhänge: "
            "<b>%{customdata[0]}</b>"
            "<extra></extra>"
        )

        customdata = df[["count"]].values


    else:
        hovertemplate = (
            "<b>%{y}</b><br><br>"
            "Durchschnittliche Zusammenhangsstärke: "
            "<b>%{x:.2f}</b><br>"
            "Basierend auf "
            "<b>%{customdata[0]}</b> Zusammenhängen"
            "<extra></extra>"
        )

        customdata = df[["count"]].values


    fig.update_traces(
        hovertemplate=hovertemplate,
        customdata=customdata
    )

    return fig


# ===========================================================================================
# Boxplot Korrelationen
# ===========================================================================================

def create_correlation_strength_boxplot(strictness_dict: dict):
    """
    Erstellt einen horizontalen Boxplot der absoluten Spearman-Korrelationen
    aller relevanten Zusammenhänge.
    """

    df = st.session_state["statistics_relevant_df"].copy()

    threshold = strictness_dict["value"]

    values = df["abs_spearman_r"]

    count = len(values)
    median = values.median()
    mean = values.mean()
    q1 = values.quantile(0.25)
    q3 = values.quantile(0.75)

    max_abs_spearman_r = values.max()
    x_scale_upper = np.ceil(max_abs_spearman_r * 1.01 * 10) / 10


    fig = go.Figure()

    fig.add_trace(
        go.Box(
            x=values,
            orientation="h",
            boxpoints=False,
            width=0.4,
            marker_color="#e49650",
            hoverinfo="skip",
            name=""
        )
    )

    fig.update_layout(
        height=200,
        width=350,
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=0
        ),
        title=dict(
            text="Verteilung Zusammenhangsstärken",
            x=0.58,
            xanchor="center",
            font=dict(size=14)
        ),
        xaxis_title="Absolute Spearman-Korrelation",
        yaxis_title="",
        showlegend=False
    )

    fig.update_xaxes(
        range=[
            threshold - 0.05,
            x_scale_upper
        ],
        title_font=dict(size=12)
    )

    fig.update_yaxes(
        showticklabels=False
    )


    fig.add_annotation(
        x=0.56,
        y=1.18,
        xref="paper",
        yref="paper",
        text=(
            f"n = <b>{count}</b>"
            f"&nbsp;&nbsp;|&nbsp;&nbsp;"
            f"Median: <b>{median:.2f}</b>"
            f"&nbsp;&nbsp;|&nbsp;&nbsp;"
            f"Mittelwert: <b>{mean:.2f}</b>"
            f"&nbsp;&nbsp;|&nbsp;&nbsp;"
            f"IQR: <b>{q1:.2f}–{q3:.2f}</b>"
        ),
        showarrow=False,
        align="center",
        font=dict(size=9)
    )

    return fig

# ===========================================================================================
# Heatmap Anzahl relevanter Korrelationen
# ===========================================================================================

def create_category_heatmap():
    """
    Erstellt eine Heatmap der Trefferquote relevanter Korrelationen zwischen
    Bildungs- und Entwicklungskategorien.
    """

    all_df = st.session_state["correlation_results_dataframe"].copy()

    relevant_df = st.session_state["statistics_relevant_df"].copy()

    all_counts = pd.crosstab(
        index=all_df["development_category"],
        columns=all_df["education_category"]
    )

    relevant_counts = pd.crosstab(
        index=relevant_df["development_category"],
        columns=relevant_df["education_category"]
    )

    relevant_counts = relevant_counts.reindex(
        index=all_counts.index,
        columns=all_counts.columns,
        fill_value=0
    )

    heatmap_df = (
        relevant_counts
        .div(all_counts)
        .mul(100)
        .round(1)
    )

    fig = px.imshow(
        heatmap_df,
        aspect="auto",
        text_auto=".1f",
        color_continuous_scale="Oranges",
        zmin=0,
        zmax=heatmap_df.max().max()
    )

    fig.update_traces(
        text=heatmap_df.map(lambda x: f"{x:.1f}%"),
        texttemplate="%{text}",
        customdata=np.dstack((relevant_counts.values, all_counts.values)),
        hovertemplate=(
            "<b>%{y}</b> ↔ <b>%{x}</b><br><br>"
            "Trefferquote: <b>%{z:.1f}%</b><br>"
            "%{customdata[0]:.0f} von %{customdata[1]:.0f} getesteten Zusammenhängen"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        height=350,
        width=350,
        margin=dict(
            l=100,
            r=20,
            t=50,
            b=0
        ),
        title=dict(
            text="Trefferquote relevanter Zusammenhänge im Vergleich",
            x=0.5,
            xanchor="center",
            font=dict(size=14)
        ),
        xaxis_title="",
        yaxis_title="",
        coloraxis_colorbar=dict(
            title=dict(
                text="Trefferquote (%)",
                font=dict(size=12)
            ),
            tickfont=dict(size=10)
        )
    )

    fig.update_xaxes(
        tickangle=-45
    )

    return fig


# ===========================================================================================
# Top Indikatoren - Barchart Kategorietyp
# ===========================================================================================

def create_top_indicator_bar_chart(
    category_type: str,
    selected_category: str,
    top_n: int = 10
):
    """
    Erstellt ein horizontales Balkendiagramm der stärksten
    Indikatorzusammenhänge innerhalb einer Kategorie.
    """

    df = st.session_state["statistics_relevant_df"].copy()

    category_column = f"{category_type}_category"

    df = df[df[category_column] == selected_category].copy()

    df = (
        df
        .sort_values("abs_spearman_r", ascending=False)
        .head(top_n)
        .copy()
    )

    df = df.sort_values(
        "abs_spearman_r",
        ascending=True
    )

    indicator_column = (
        "education_indicator"
        if category_type == "education"
        else "development_indicator"
    )

    df["indicator_short"] = (
        df[indicator_column]
        .str.slice(0, 35)
        .where(
            df[indicator_column].str.len() <= 35,
            df[indicator_column].str.slice(0, 35) + "..."
        )
    )

    fig = px.bar(
        df,
        x="abs_spearman_r",
        y="indicator_short",
        orientation="h",
        custom_data=[
            "education_indicator",
            "development_indicator",
            "spearman_r",
            "countries"
        ]
    )

    fig.update_traces(
        marker_color="#e49650",
        hovertemplate=(
            "<b>%{y}</b><br><br>"
            "Bildungsindikator:<br>"
            "%{customdata[0]}<br><br>"
            "Entwicklungsindikator:<br>"
            "%{customdata[1]}<br><br>"
            "Spearman r: <b>%{customdata[2]:.2f}</b><br>"
            "Absolute Stärke: <b>%{x:.2f}</b><br>"
            "Länder: %{customdata[3]}"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        height=320,
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=30
        ),
        title=dict(
            text=f"Top Zusammenhänge: {selected_category}",
            x=0.5,
            xanchor="center",
            font=dict(size=14)
        ),
        xaxis_title="Absolute Spearman-Korrelation",
        yaxis_title="",
        showlegend=False
    )

    fig.update_xaxes(
        range=[
            0,
            df["abs_spearman_r"].max() * 1.1
        ]
    )

    return fig