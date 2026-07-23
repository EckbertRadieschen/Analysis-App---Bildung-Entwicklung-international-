import streamlit as st

from app.selectors import get_statistics_category_options



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
    # Ansicht
    # ============================================================================================

    view_options = ["Gesamtübersicht", "Einzelkategorien"]

    selected_view = st.sidebar.radio(
        "Ansicht",
        options=view_options,
        key="statistics_view"
    )

    details_selected = selected_view == "Einzelkategorien"


    # ============================================================================================
    # Entwicklungskategorie
    # ============================================================================================

    st.sidebar.divider()

    st.sidebar.markdown("#### Entwicklung")

    development_categories = get_statistics_category_options("development")
    
    selected_development_category = st.sidebar.selectbox(
        "Kategorie",
        options=development_categories,
        format_func=lambda x: x["name"],
        key="statistics_development_category",
        disabled=not details_selected
    )

    # ============================================================================================
    # Bildungskategorie
    # ============================================================================================

    st.sidebar.divider()

    st.sidebar.markdown("#### Bildung")

    education_categories = get_available_statistics_categories(correlation_results, "education")
    

    selected_education_category = st.sidebar.selectbox(
        "Kategorie",
        options=education_categories,
        format_func=lambda x: x["name"],
        key="statistics_education_category",
        disabled=not details_selected
    )


    # ============================================================================================
    # Bewertung
    # ============================================================================================

    st.sidebar.divider()

    st.sidebar.markdown("#### Bewertung")

    evaluation_options = ["Anzahl Zusammenhänge", "Stärke der Zusammenhänge"]

    selected_evaluation = st.sidebar.selectbox(
        "Bewertung",
        options=evaluation_options,
        key="statistics_evaluation"
    )

    st.session_state["selected_statistics_view"] = selected_view
    st.session_state["selected_statistics_development_category"] = selected_development_category
    st.session_state["selected_statistics_education_category"] = selected_education_category
    st.session_state["selected_statistics_evaluation"] = selected_evaluation
    