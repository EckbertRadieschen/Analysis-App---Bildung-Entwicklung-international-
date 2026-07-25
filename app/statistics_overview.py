import plotly.express as px
import streamlit as st

from src.visuals import (
    create_correlation_strength_boxplot, 
    create_category_statistics_bar_chart, 
    create_category_heatmap
)

def statistics_overview_content():

    evaluation = st.session_state["statistics_evaluation"]
    strictness = st.session_state["statistics_strictness"]

    fig_dev = create_category_statistics_bar_chart("development", evaluation, strictness)
    fig_edu = create_category_statistics_bar_chart("education", evaluation, strictness)

    evaluation_type = evaluation["label"]

    sub_subdiv = """"""
    if evaluation_type == "Anteil relevanter Zusammenhänge":
        subtitle = "bezogen auf die Gesamtzahl der getesteten Zusammenhänge"
    elif evaluation_type == "Durchschnittliche Zusammenhangsstärke":
        subtitle = "Durchschnittliche 'Spearman'-Korrleation (Interpretation s.u.)"
    elif evaluation_type == "Kumulierte Zusammenhangsstärke": 
        subtitle = "Summe der absoluten Spearman-Korrelationskoeffizienten aller relevanten Zusammenhänge"
        sub_subtitle = "(Höhere Werte entstehen durch mehr und/oder stärkere Zusammenhänge)"
        sub_subdiv = f"""<div class="custom-sub_subtitle">{sub_subtitle}</div>"""

    st.markdown(
        f"""
        <div class="custom-subheader">
            <div class="custom-title">Kategorien - {evaluation_type}</div>
            <div class="custom-subtitle">{subtitle}</div>
            {sub_subdiv}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    barchart_blank_1, barchart_column_1, barchart_column_2, barchart_blank_2 = st.columns([1, 12, 12, 1])

    with barchart_column_1:
        st.plotly_chart(
            fig_dev,
            key="statistics_dev_category_bar",
            config={
                "displayModeBar": False
            }
        )
    with barchart_column_2:    
        st.plotly_chart(
            fig_edu,
            key="statistics_edu_category_bar",
            config={
                "displayModeBar": False
            }   
        )


    bp_blank_1, boxplot_column, heatmap_column, bp_blank_2 = st.columns([2, 6, 12, 1])

    with boxplot_column:
        fig_boxplot = create_correlation_strength_boxplot(strictness)
        st.plotly_chart(
            fig_boxplot,
            key="statistics_category_boxplot",
            config={
                "displayModeBar": False
            }
        )


    with heatmap_column:
        fig_heatmap = create_category_heatmap()
        st.plotly_chart(
            fig_heatmap,
            key="statistics_category_heatmap",
            config={
                "displayModeBar": False
            }
        )