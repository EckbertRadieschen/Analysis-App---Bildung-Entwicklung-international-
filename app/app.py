import streamlit as st

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.paths import (
    DEVELOPMENT_CONFIG,
    EDUCATION_CONFIG,
    CORRELATION_RESULTS
)
from src.preparations import load_config
from src.analysis import load_correlation_results

from app.selectors import (all_sidebar_selected)

from utils.hilfsfunktionen import get_max_year_from_config

from app.markdown import apply_markdown

from app.navigation import navigation_content
from app.analytic_tool import analytic_tool
from app.intro_page import intro_page
from app.statistic_page import statistic_page

# =======================================================================================================
# =======================================================================================================

apply_markdown()

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# =======================================================================================================
# =======================================================================================================

st.session_state["dev_config"] = (development_config := load_config(DEVELOPMENT_CONFIG))
st.session_state["edu_config"] = (education_config := load_config(EDUCATION_CONFIG))

st.session_state["dev_meta"] = (development_meta := development_config["meta_data"])
st.session_state["edu_meta"] = (education_meta := education_config["meta_data"])

st.session_state["dev_indicators_config"] = (development_indicators_from_config := development_config["indicators"])
st.session_state["edu_indicators_config"] = (education_indicators_from_config := education_config["indicators"])


st.session_state["dev_max_year"] = (dev_max_year := get_max_year_from_config(development_config))
st.session_state["edu_max_year"] = (edu_max_year := get_max_year_from_config(education_config))

if not "navigation_choice" in st.session_state:
    st.session_state["navigation_choice"] = "Intro-Seite"

all_sidebar_selected()


# ============================================================================================
# Navigationsleiste
# ============================================================================================

navigation_content()


# ============================================================================================
# Hauptbereich
# ============================================================================================
if (not "correlation_results_dataframe" in st.session_state) or (st.session_state["correlation_results_dataframe"] is None):
        st.session_state["correlation_results_dataframe"] = load_correlation_results(CORRELATION_RESULTS)

if st.session_state["navigation_choice"] == "Intro-Seite":
    intro_page()

elif st.session_state["navigation_choice"] == "Analyse-Tool":
    analytic_tool()

elif st.session_state["navigation_choice"] == "Statistik-Seite":
    statistic_page()