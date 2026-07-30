import streamlit as st

from app.selectors import (
    get_statistics_category_options,
    get_change_offset_options 
)

from src.paths import DEVELOPMENT_CONFIG

from src.preparations import load_config
from src.analysis import (
    update_statistics_data
)

def statistics_sidebar_content():

    # ============================================================================================
    # Titel
    # ============================================================================================

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
    # Ansicht
    # ============================================================================================

    view_options = ["Gesamtübersicht", "Einzelkategorien"]

    selected_view = st.sidebar.radio(
        "Ansicht",
        options=view_options,
        horizontal=True,
        key="statistics_view"
    )

    details_selected = selected_view == "Einzelkategorien"


    # ============================================================================================
    # Bildungsvorlauf und Vergleichszeitraum
    # ============================================================================================
    
    change_column, lag_column = st.sidebar.columns([1, 2])

    with change_column:
        development_config = load_config(DEVELOPMENT_CONFIG)
        change_offsets = get_change_offset_options(development_config)

        selected_change_offset = st.selectbox(
            "Vergleichszeitraum",
            options=change_offsets,
            index=0,
            format_func=lambda x: f"{x} Jahre",
            key="statistics_change_offset",
            on_change=update_statistics_data
        )   

    with lag_column:
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
                    
        selected_lag_factor = st.selectbox(
            "Bildungsvorlauf",
            options=lag_options,
            index=0,
            format_func=lambda x: x["label"],
            key="statistics_lag_factor",
            on_change=update_statistics_data
        )



    # ============================================================================================
    # Bewertung
    # ============================================================================================

    st.sidebar.divider()

    evaluation_options = evaluation_options = [
        {
            "label": "Anteil relevanter Zusammenhänge",
            "value_column": "relevance_ratio"
        },
        {
            "label": "Kumulierte Zusammenhangsstärke",
            "value_column": "sum_abs_r"
        },
        {
            "label": "Durchschnittliche Zusammenhangsstärke",
            "value_column": "mean_abs_r"
        }
    ]

    selected_evaluation = st.sidebar.selectbox(
        "Bewertung nach",
        options=evaluation_options,
        format_func=lambda x: x["label"],
        index=0,
        key="statistics_evaluation"
    )


    strictness_options = [
        {"value": 0.3, "label": "geringe Strenge (r > 0.3)"}, 
        {"value": 0.5, "label": "mittlere Strenge (r > 0.5)"}, 
        {"value": 0.7, "label": "hohe Strenge (r > 0.7)"}
    ]

    selected_strictness = st.sidebar.selectbox(
        "Strenge der Bewertung (nach 'Spearman'-Koeffizient [r])",
        options=strictness_options,
        index=1,
        format_func=lambda x: x["label"],
        key="statistics_strictness",
        on_change=update_statistics_data
    )

    if not "statistics_base_df" in st.session_state:
        update_statistics_data()

    # ============================================================================================
    # Entwicklungskategorie
    # ============================================================================================

    st.sidebar.divider()

    development_categories = get_statistics_category_options("development")
    
    selected_development_category = st.sidebar.selectbox(
        "Entwicklungskategorie",
        options=development_categories,
        key="statistics_development_category",
        disabled=not details_selected
    )

    # ============================================================================================
    # Bildungskategorie
    # ============================================================================================

    education_categories = get_statistics_category_options("education")
    

    selected_education_category = st.sidebar.selectbox(
        "Bildungskategorie",
        options=education_categories,
        key="statistics_education_category",
        disabled=not details_selected
    )


    st.session_state["selected_statistics_view"] = selected_view
    st.session_state["selected_statistics_development_category"] = selected_development_category
    st.session_state["selected_statistics_education_category"] = selected_education_category
    st.session_state["selected_statistics_evaluation"] = selected_evaluation
    st.session_state["selected_statistics_strictness"] = selected_strictness