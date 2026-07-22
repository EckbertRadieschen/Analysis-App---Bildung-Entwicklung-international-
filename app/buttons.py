import streamlit as st


def choose_analytics_tool():
    st.session_state["navigation_choice"] = "Analyse-Tool"

def choose_statistics_page():
    st.session_state["navigation_choice"] = "Statistik-Seite"

# =================================================================

def choose_top():
    st.session_state["top_bottom_choice"] = "Top 10"

def choose_bottom():
    st.session_state["top_bottom_choice"] = "Bottom 10"

# =================================================================

def choose_development():
    st.session_state["main_bar_source_choice"] = "Entwicklungsvariable"

def choose_education():
    st.session_state["main_bar_source_choice"] = "Bildungsindikator"

def choose_comparison():
    st.session_state["main_bar_source_choice"] = "Zusammenhang"
