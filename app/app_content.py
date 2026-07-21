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