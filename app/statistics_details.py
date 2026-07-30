import streamlit as st

from src.visuals import (
    create_top_indicator_bar_chart, 
    create_indicator_combination_bar_chart,
    choose_donut_charts
)


def statistics_details_content():
    development_category = st.session_state["statistics_development_category"]
    education_category = st.session_state["statistics_education_category"]

    evaluation_dict = st.session_state["statistics_evaluation"]
    evaluation_type = evaluation_dict["label"]

    sub_subdiv = ""

    if evaluation_type == "Anteil relevanter Zusammenhänge":
        subtitle = "bezogen auf die Gesamtzahl der getesteten Zusammenhänge"

    elif evaluation_type == "Durchschnittliche Zusammenhangsstärke":
        subtitle = "Durchschnittliche 'Spearman'-Korrelation (Interpretation s.u.)"

    elif evaluation_type == "Kumulierte Zusammenhangsstärke":
        subtitle = "Summe der absoluten Spearman-Korrelationskoeffizienten aller relevanten Zusammenhänge"

        sub_subtitle ="(Höhere Werte entstehen durch mehr und/oder stärkere Zusammenhänge)"

        sub_subdiv = f"""<div class="custom-sub_subtitle">{sub_subtitle}</div>"""

    st.markdown(
        f"""
        <div class="custom-subheader">
            <div class="custom-title">Kategorie Detailansicht - {evaluation_type}</div>
            <div class="custom-subtitle">{subtitle}</div>
            {sub_subdiv}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    with st.spinner("Indikator-Daten werden geladen..."):
        fig_dev = create_top_indicator_bar_chart("development", development_category, evaluation_dict)
        fig_edu = create_top_indicator_bar_chart("education", education_category, evaluation_dict)

        col_blank_1, col_dev, col_edu, col_blank_2 = st.columns([1, 12, 12, 1])

        with col_dev:
            if fig_dev:
                st.plotly_chart(
                    fig_dev,
                    key="statistics_dev_category_bar",
                    config={
                        "displayModeBar": False
                    }
                )

            else:
                st.info(
                    "Für diese Entwicklungskategorie wurden keine relevanten Entwicklungsindikatoren gefunden."
                )

        with col_edu:
            if fig_edu:
                st.plotly_chart(
                    fig_edu,
                    key="statistics_edu_category_bar",
                    config={
                        "displayModeBar": False
                    }
                )
            else:
                st.info(
                    "Für diese Bildungskategorie wurden keine relevanten Entwicklungsindikatoren gefunden."
                )

        col_blank_3, col_pie, col_combi, col_blank_4 = st.columns([1, 12, 12, 1])

        selected_development_category = st.session_state["statistics_development_category"]
        selected_education_category = st.session_state["statistics_education_category"]

        with col_pie:
            statistics_modes = [selected_education_category, selected_development_category]

            selected_statistics_mode = st.selectbox(
                "Kategorie für Verteilung",
                options=statistics_modes,
                index=0,
                key="statistics_mode"
            )

            st.markdown(
                f"""
                <div class='chart-title'>Verteilung der Zusammenhänge in der Kategorie {selected_statistics_mode}</div>
                """,
                unsafe_allow_html=True
            )

            fig_distribution_pie, fig_interpretation_pie = choose_donut_charts()

            col_distribution, col_interpretation = st.columns([6, 6])

            with col_distribution:
                st.plotly_chart(
                    fig_distribution_pie,
                    key="statistics_pie_distribution",
                    config={
                        "displayModeBar": False
                    }
                )

            with col_interpretation:
                if fig_interpretation_pie:
                    st.plotly_chart(
                        fig_interpretation_pie,
                        key="statistics_pie_interpretation",
                        config={
                            "displayModeBar": False
                        }
                    )
                else:
                    st.info(
                        "Keine relevanten Zusammenhänge gefunden."
                    )

        with col_combi:
            interpretation_options = [
                {
                    "label": "Alle",
                    "value": "all"
                },
                {
                    "label": "Vorzeichen intuitiv",
                    "value": "normal"
                },
                {
                    "label": "Vorzeichen kritisch prüfen",
                    "value": "inverted"
                }
            ]

            selected_interpretation = st.selectbox(
                "Interpretation",
                options=interpretation_options,
                index=0,
                format_func=lambda x: x["label"],
                key="statistics_indicator_combination_interpretation"
            )

            fig_combi = create_indicator_combination_bar_chart(
                education_category, 
                development_category, 
                interpretation_filter=selected_interpretation["value"]
            )

            if fig_combi:
                st.plotly_chart(
                    fig_combi,
                    key="statistics_combi_indicator_bar",
                    config={
                        "displayModeBar": False
                    }
                )
            else:
                st.info(
                    "Für diese Kategorie-Kombination wurden keine relevanten Zusammenhänge gefunden."
                )