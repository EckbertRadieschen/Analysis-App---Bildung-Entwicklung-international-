import streamlit as st
import pandas as pd

from app.selectors import get_statistics_category_options



def load_category_statistics(strictness: dict) -> None:
    """
    Erstellt einen DataFrame mit Kennzahlen pro Bildungs- und
    Entwicklungskategorie.

    Die Correlation Results werden anhand der gewählten Strenge
    bewertet. Anschließend werden Kennzahlen pro Kategorie berechnet.
    """

    df = st.session_state["correlation_results_dataframe"].copy()

    threshold = strictness["value"]

    filtered_df = df[df["spearman_r"].abs() >= threshold].copy()

    rows = []

    for category_type in ["development", "education"]:

        category_column = f"{category_type}_category"

        all_groups = df.groupby(category_column)

        filtered_groups = filtered_df.groupby(category_column)


        for category, all_group in all_groups:
            if category in filtered_groups.groups:
                relevant_group = filtered_groups.get_group(category)
            else:
                continue

            rows.append(
                {
                    "category_type": category_type,
                    "category": category,

                    "count": len(relevant_group),
                    "relevance_ratio": len(relevant_group) / len(all_group),
                    "sum_abs_r": relevant_group["spearman_r"].abs().sum(),
                    "mean_abs_r": relevant_group["spearman_r"].abs().mean(),

                    "significant_count": (relevant_group["spearman_p"] < 0.05).sum(),
                    "median_abs_r": relevant_group["spearman_r"].abs().median(),
                }
            )

    st.session_state["category_statistics"] = pd.DataFrame(rows)

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
        key="statistics_view"
    )

    details_selected = selected_view == "Einzelkategorien"

    # ============================================================================================
    # Bewertung
    # ============================================================================================

    st.sidebar.divider()

    st.sidebar.markdown("#### Bewertung")

    evaluation_options = evaluation_options = [
        {
            "label": "Anteil relevanter Zusammenhänge",
            "value_column": "relevance_ratio"
        },
        {
            "label": "Gesamtstärke der Zusammenhänge",
            "value_column": "sum_abs_r"
        },
        {
            "label": "Durchschnittliche Stärke",
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
        {"value": 0.3, "label": "geringe Strenge"}, 
        {"value": 0.5, "label": "mittlere Strenge"}, 
        {"value": 0.7, "label": "hohe Strenge"}
    ]

    selected_strictness = st.sidebar.selectbox(
        "Strenge der Bewertung",
        options=strictness_options,
        index=1,
        format_func=lambda x: x["label"],
        key="statistics_strictness"
    )

    if not "category_statistics" in st.session_state:
        load_category_statistics(selected_strictness)

    # ============================================================================================
    # Entwicklungskategorie
    # ============================================================================================

    st.sidebar.divider()

    st.sidebar.markdown("#### Entwicklung")

    development_categories = get_statistics_category_options("development")
    
    selected_development_category = st.sidebar.selectbox(
        "Kategorie",
        options=development_categories,
        key="statistics_development_category",
        disabled=not details_selected
    )

    # ============================================================================================
    # Bildungskategorie
    # ============================================================================================

    st.sidebar.divider()

    st.sidebar.markdown("#### Bildung")

    education_categories = get_statistics_category_options("education")
    

    selected_education_category = st.sidebar.selectbox(
        "Kategorie",
        options=education_categories,
        key="statistics_education_category",
        disabled=not details_selected
    )


    st.session_state["selected_statistics_view"] = selected_view
    st.session_state["selected_statistics_development_category"] = selected_development_category
    st.session_state["selected_statistics_education_category"] = selected_education_category
    st.session_state["selected_statistics_evaluation"] = selected_evaluation
    st.session_state["selected_statistics_strictness"] = selected_strictness
    