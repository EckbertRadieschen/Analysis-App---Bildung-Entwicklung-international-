import streamlit as st

from src.visuals import create_top_indicator_bar_chart


def statistics_details_content():
    selected_development_category = st.session_state["selected_statistics_development_category"]
    selected_education_category = st.session_state["selected_statistics_education_category"]

    fig_dev = create_top_indicator_bar_chart("development", selected_development_category)
    fig_edu = create_top_indicator_bar_chart("education", selected_education_category)

    st.plotly_chart(
        fig_dev,
        key="statistics_dev_category_bar",
        config={
            "displayModeBar": False
        }
    )

    st.plotly_chart(
        fig_edu,
        key="statistics_dev_category_bar",
        config={
            "displayModeBar": False
        }
    )