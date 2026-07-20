import streamlit as st

def choose_top():
    st.session_state["top_bottom_choice"] = "top"

def choose_bottom():
    st.session_state["top_bottom_choice"] = "bottom"

# =================================================================

def choose_development():
    st.session_state["main_bar_source_choice"] = "development"

def choose_education():
    st.session_state["main_bar_source_choice"] = "education"

def choose_comparison():
    st.session_state["main_bar_source_choice"] = "comparison"