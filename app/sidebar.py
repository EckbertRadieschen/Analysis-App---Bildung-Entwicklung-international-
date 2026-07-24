import streamlit as st

from src.preparations import load_config
from app.selectors import (
    get_available_development_categories,
    get_available_development_category_indicators,
    get_available_education_categories,
    get_available_education_indicators,
    get_change_offset_options,
    reset_development_indicator,
    reset_education_category,
    reset_education_indicator
)

def sidebar_content ():

    development_config = st.session_state["dev_config"] 
    education_config = st.session_state["edu_config"]  

    development_meta = st.session_state["dev_meta"]  
    education_meta = st.session_state["edu_meta"] 

    development_indicators_from_config = st.session_state["dev_indicators_config"] 
    education_indicators_from_config = st.session_state["edu_indicators_config"] 

    dev_max_year = st.session_state["dev_max_year"] 
    edu_max_year = st.session_state["edu_max_year"]

    with st.sidebar.container(key="sidebar_title_container"):
        st.markdown(
            """
            <div class="wrapper-title">
                Auswahl
            </div>
            """,
            unsafe_allow_html=True
        )


    # ============================================================================================
    # Development Selectors
    # ============================================================================================

    st.sidebar.markdown("#### Entwicklungsvariable")

    development_categories = get_available_development_categories(development_config)

    selected_development_category = st.sidebar.selectbox(
        "Kategorie",
        options=development_categories,
        index=None,
        placeholder="Bitte Kategorie auswählen",
        format_func=lambda x: x["name"],
        key="selected_development_category",
        on_change=reset_development_indicator
    )

    development_indicators = get_available_development_category_indicators(development_config, selected_development_category)

    selected_development_indicator = st.sidebar.selectbox(
        "Indikator",
        options=development_indicators,
        index=None,
        placeholder=(
            "Bitte Indikator auswählen" 
            if selected_development_category is not None
            else "Bitte zunächst Kategorie auswählen"
        ),
        format_func=lambda x: x["name"],
        disabled=selected_development_category is None,
        key="selected_development_indicator"
    )

    change_offsets = get_change_offset_options(development_config)

    selected_change_offset = st.sidebar.selectbox(
        "Vergleichszeitraum",
        options=change_offsets,
        index=None,
        placeholder="Bitte Zeitraum auswählen",
        format_func=lambda x: f"{x} Jahre",
        key="selected_change_offset",
        on_change=reset_education_category
    )

    # ============================================================================================
    # Education Selectors
    # ============================================================================================

    st.sidebar.divider()

    st.sidebar.markdown("#### Bildungsindikator")

    lag_options = [
        {
            "factor": 1,
            "label": "Bildungsrelevanz nach kurzer Verzögerung"
        },
        {
            "factor": 2,
            "label": "Bildungsrelevanz nach langer Verzögerung"
        }
    ]
                
    selected_lag_factor = st.sidebar.selectbox(
        "Bildungsvorlauf",
        options=lag_options,
        index=None,
        placeholder="Bitte Bildungsvorlauf auswählen",
        format_func=lambda x: x["label"],
        key="selected_lag_factor",
        on_change=reset_education_category
    )

    education_categories = (
        []
        if not selected_lag_factor
        else get_available_education_categories(
            education_config,
            selected_change_offset,
            selected_lag_factor["factor"],
            education_meta["min_available_countries"]
        )
    )

    selected_education_category = st.sidebar.selectbox(
        "Kategorie",
        options=education_categories,
        index=None,
        placeholder=(
            "Bitte Kategorie auswählen" 
            if (
                selected_change_offset is not None
                and selected_lag_factor is not None
            )
            else "Bitte zunächst Bildungsvorlauf auswählen" 
            if selected_change_offset is not None
            else "Bitte zunächst Vergleichszeitraum auswählen"
        ),
        format_func=lambda x: x["name"],
        disabled=(
            selected_change_offset is None
            or selected_lag_factor is None
        ),
        key="selected_education_category",
        on_change=reset_education_indicator
    )


    education_indicators = (
        []
        if not selected_lag_factor
        else get_available_education_indicators(
            education_config, 
            selected_education_category,
            selected_change_offset,
            selected_lag_factor["factor"],
            education_meta["min_available_countries"]
        )
    )

    selected_education_indicator = st.sidebar.selectbox(
        "Indikator",
        options=education_indicators,
        index=None,
        placeholder=(
            "Bitte Indikator auswählen" 
            if (
                selected_education_category is not None
                and selected_change_offset is not None
                and selected_lag_factor is not None
            )
            else "Bitte zunächst Kategorie auswählen"
            if selected_change_offset is not None
            else "---"
        ),
        format_func=lambda x: x["name"],
        disabled=(
            selected_education_category is None
            or selected_change_offset is None
            or selected_lag_factor is None
        ),
        key="selected_education_indicator"
    )


