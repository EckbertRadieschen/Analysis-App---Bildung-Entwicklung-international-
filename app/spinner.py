import streamlit as st

from src.analysis import create_analysis_frames
from src.visuals import choose_main_chart

from app.save_combinations import get_or_create_correlation_result

from src.paths import CORRELATION_RESULTS


def spinner_content():

    development_config = st.session_state["dev_config"]
    education_config = st.session_state["edu_config"]

    selected_development_indicator = st.session_state["selected_development_indicator"]
    selected_education_indicator = st.session_state["selected_education_indicator"]
    selected_development_category = st.session_state["selected_development_category"]
    selected_education_category = st.session_state["selected_education_category"]
    selected_change_offset = st.session_state["selected_change_offset"]


    st.session_state["main_chart"] = None

    blank_spinner_1, spinner_column, blank_spinner_2 = st.columns([1, 3, 1])
    with spinner_column:
        with st.spinner("Analysedaten werden erstellt..."):

            create_analysis_frames(
                selected_development_indicator,
                selected_education_indicator,
                development_config,
                education_config
            )

            correlation_result = get_or_create_correlation_result(
                    selected_development_indicator["key"],
                    selected_education_indicator["key"],
                    selected_development_category,
                    selected_education_category,
                    selected_change_offset,
                    st.session_state["comparison_frame"],
                    CORRELATION_RESULTS
            )

            st.session_state["main_chart"] = choose_main_chart()

            return correlation_result