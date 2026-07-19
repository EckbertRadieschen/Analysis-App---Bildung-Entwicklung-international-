import streamlit as st
import pandas as pd

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.paths import (
    DEVELOPMENT_CONFIG,
    EDUCATION_CONFIG
)
from src.preparations import load_config
from app.selectors import (
    get_available_categories,
    get_available_category_indicators,
    get_change_offset_options    
)

from app.markdown import apply_markdown

# =======================================================================================================
# =======================================================================================================

apply_markdown()

development_config = load_config(DEVELOPMENT_CONFIG)
education_config = load_config(EDUCATION_CONFIG)

st.title("Bildung und Länderentwicklung")

st.sidebar.header("Auswahl")
st.sidebar.divider()

# ============================================================================================
# Development Selectors
# ============================================================================================

st.sidebar.subheader("Entwicklung")

development_categories = get_available_categories(development_config)

selected_development_category = st.sidebar.selectbox(
    "Kategorie",
    options=development_categories,
    index=None,
    placeholder="Bitte Kategorie auswählen",
    format_func=lambda x: x["name"],
    key="selected_development_category"
)

development_indicators = get_available_category_indicators(development_config, selected_development_category)


selected_development_indicator = st.sidebar.selectbox(
    "Indikator",
    options=development_indicators,
    index=None,
    placeholder=(
        "Bitte Indikator auswählen" 
        if selected_development_category is not None
        else "Bitte zunächst Kategorie auswählen"
    ),
    format_func=lambda x: x["short_description"],
    disabled=selected_development_category is None
)

change_offsets = get_change_offset_options(development_config)

selected_change_offset = st.sidebar.selectbox(
    "Vergleichszeitraum",
    options=change_offsets,
    index=None,
    placeholder=(
        "Bitte Zeitraum auswählen"
        if selected_development_indicator is not None
        else "Bitte zunächst Indikator auswählen"
    ),
    format_func=lambda x: f"{x} Jahre",
    disabled=selected_development_indicator is None
)

# ============================================================================================
# Education Selectors
# ============================================================================================

st.sidebar.subheader("Bildung")

development_categories = get_available_categories(development_config)

selected_development_category = st.sidebar.selectbox(
    "Kategorie",
    options=development_categories,
    index=None,
    placeholder="Bitte Kategorie auswählen",
    format_func=lambda x: x["name"],
    key="selected_development_category"
)

development_indicators = get_available_category_indicators(development_config, selected_development_category)


selected_development_indicator = st.sidebar.selectbox(
    "Indikator",
    options=development_indicators,
    index=None,
    placeholder=(
        "Bitte Indikator auswählen" 
        if selected_development_category is not None
        else "Bitte zunächst Kategorie auswählen"
    ),
    format_func=lambda x: x["short_description"],
    disabled=selected_development_category is None
)



if selected_change_offset is not None:
    st.write(
        "Auswahl:",
        selected_change_offset
    )









