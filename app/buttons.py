import streamlit as st

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