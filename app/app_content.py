import streamlit as st
from src.analysis import get_analysis_data

def set_main_chart_title (edu_config: dict):
    dev_indicator_dict, edu_indicator_dict, change_offset = get_analysis_data()

    source = st.session_state.get("main_bar_source_choice", "Entwicklungsvariable")

    edu_indicator_code = edu_indicator_dict["key"]

    lag = (
        edu_config["indicators"][edu_indicator_code]["recommended_lag"] 
        if source == "Bildungsindikator" 
        else 0
    )

    max_year = edu_config["meta_data"]["max_year"]
    comparison_year = max_year - change_offset - lag
    comparison_period = f"ca. {comparison_year} - {max_year}"

    dev_description = dev_indicator_dict["name"].split('(')[0]
    edu_description = edu_indicator_dict["name"].split('(')[0]

    if source == "Entwicklungsvariable":
        title = f"{dev_description}\nTrend im Zeitraum {comparison_period}"

    elif source == "Bildungsindikator":
        title = f"{edu_description}\nBildungsjahr ca. {comparison_year}"

    else:
        title = f"Zusammenhang:\n{edu_description} - vs - {dev_description}"

    return title


# ==================================================================================
# Interpretiert Korrelationswerte
# ==================================================================================

def interpret_correlation(value: float) -> str:

    abs_value = abs(value)

    if abs_value < 0.2:
        return "sehr geringer Zusammenhang"
    elif abs_value < 0.4:
        return "geringer Zusammenhang"
    elif abs_value < 0.6:
        return "moderater Zusammenhang"
    else:
        return "starker Zusammenhang"


# ==================================================================================
# Stellt die Korrelationswerte der aktuellen Kombination dar
# ==================================================================================

def display_correlation_info(correlation_result: dict):
    """
    Zeigt Korrelationskennzahlen inklusive Stärke des Zusammenhangs an.
    """

    pearson_r = correlation_result["pearson"]["r"]
    spearman_r = correlation_result["spearman"]["r"]
    countries = correlation_result["countries"]

    st.markdown(
        f"""
        <div class="stats-container">
            <div class="medium-title">
                Korrelationsanalyse
            </div>
            <div class="small-text">
                <b>Pearson:</b> {pearson_r:.3f}<br>
                {interpret_correlation(pearson_r)}<br><br>
                <b>Spearman:</b> {spearman_r:.3f}<br>
                {interpret_correlation(spearman_r)}<br><br>
                <b>Anzahl Länder:</b> {countries}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )