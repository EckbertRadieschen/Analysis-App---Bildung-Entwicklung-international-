import streamlit as st

from app.selectors import get_available_statistics_categories



def statistics_sidebar_content():

    correlation_results = st.session_state["correlation_results_dataframe"]

    development_config = st.session_state["dev_config"]
    education_config = st.session_state["edu_config"]


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
    # Entwicklungskategorie
    # ============================================================================================

    st.sidebar.markdown("#### Entwicklung")

    development_categories = (
        get_available_statistics_categories(
            correlation_results,
            "development"
        )
    )

    development_categories = [
        {
            "category": "all",
            "name": "Alle"
        }
    ] + development_categories


    selected_development_category = st.sidebar.selectbox(
        "Kategorie",
        options=development_categories,
        format_func=lambda x: x["name"],
        key="statistics_development_category"
    )


    # ============================================================================================
    # Bildungskategorie
    # ============================================================================================

    st.sidebar.divider()

    st.sidebar.markdown("#### Bildung")

    education_categories = (
        get_available_statistics_categories(
            correlation_results,
            "education"
        )
    )

    education_categories = [
        {
            "category": "all",
            "name": "Alle"
        }
    ] + education_categories


    selected_education_category = st.sidebar.selectbox(
        "Kategorie",
        options=education_categories,
        format_func=lambda x: x["name"],
        key="statistics_education_category"
    )


    # ============================================================================================
    # Auswertung
    # ============================================================================================

    st.sidebar.divider()

    st.sidebar.markdown("#### Bewertung")

    evaluation_options = [
        {
            "key": "count",
            "name": "Anzahl Zusammenhänge"
        },
        {
            "key": "strength",
            "name": "Stärke der Zusammenhänge"
        }
    ]

    selected_evaluation = st.sidebar.selectbox(
        "Bewertung",
        options=evaluation_options,
        format_func=lambda x: x["name"],
        key="statistics_evaluation"
    )

    st.session_state["selected_statistics_development_category"] = selected_development_category
    st.session_state["selected_statistics_education_category"] = selected_education_category
    st.session_state["selected_statistics_evaluation"] = selected_evaluation