import streamlit as st

from src.paths import (
    CORRELATION_RESULTS
)

from app.app_content import set_main_chart_title, display_correlation_info

from app.save_combinations import load_json_if_exists

from app.sidebar import sidebar_content
from app.popovers import popovers_content
from app.spinner import spinner_content


def analytic_tool():

    education_config = st.session_state["edu_config"]

    if "correlation_results_dataframe" in st.session_state:
        st.session_state["correlation_results_dataframe"] = None

    # ============================================================================================
    # Sidebar
    # ============================================================================================

    sidebar_content()


    # ============================================================================================
    # Hauptbereich - Popovers
    # ============================================================================================

    if st.session_state["are_all_sidebar_selectors"]:

        selected_development_indicator = st.session_state["selected_development_indicator"]
        selected_education_indicator = st.session_state["selected_education_indicator"]
        selected_change_offset = st.session_state["selected_change_offset"]

        # =======================================================================================
        # Pop-Overs
        # =======================================================================================

        popovers_content()

        st.divider()

        title, subtitle = set_main_chart_title(education_config)
        st.markdown(
            f"""
            <div class="custom-subheader">
                <div class="custom-title">{title}</div>
                <div class="custom-subtitle">{subtitle}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    else:
        header_blank1, header_column, header_blank2 = st.columns([1, 7, 1])
        with header_column:
            st.title("Willkommen im Analyse-Tool")

    st.divider()

    # ============================================================================================
    # Hauptbereich
    # ============================================================================================

    if st.session_state["are_all_sidebar_selectors"]:

        if "correlation_results" not in st.session_state:
            st.session_state["correlation_results"] = load_json_if_exists(
                CORRELATION_RESULTS
            )

        spinner_content()

        if "main_chart" in st.session_state and st.session_state["main_chart"] is not None:
            fig = st.session_state["main_chart"]

        # ====================================================================
        # Visualisierung

            if st.session_state.get("main_bar_source_choice", "Entwicklungsvariable") == "Zusammenhang":
                sc_blank_1, scatter_column, sc_blank_2, statistic_column, sc_blank_3 = st.columns([1, 4, 0.5, 2, 1])
                with scatter_column:
                    st.plotly_chart(fig)
                with statistic_column:
                    display_correlation_info(st.session_state["current_correlation_result"])
            else:
                bar_blank_1, bar_column, bar_blank_2 = st.columns([0.5, 3, 0.5])

                with bar_column:
                    st.plotly_chart(fig)

    else:
        des_blank1, description_column, des_blank2 = st.columns([1, 5, 1])
        with description_column:
            st.markdown("""
            <br>
            <br>
            <br>
            Wählen Sie zur Analyse über die Sidebar eine beliebige Konfiguration<br>
            von Entwicklungs- und Bildungsindikatoren sowie einen Vergleichszeitraum,<br>
            über den der Entwicklungstrend berechnet werden soll.<br><br>
            Beachten Sie, dass je nach Vergleichszeitraum eine andere Auswahl<br>
            an Bildungsindikatoren verfügbar sein kann.
            """, unsafe_allow_html=True)