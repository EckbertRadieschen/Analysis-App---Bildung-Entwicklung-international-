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
    get_available_change_offsets
)

development_config = load_config(DEVELOPMENT_CONFIG)
education_config = load_config(EDUCATION_CONFIG)

st.title("Bildung und Länderentwicklung")

st.sidebar.header("Auswahl")

development_categories = get_available_categories(development_config)

selected_development_category = st.sidebar.selectbox(
    "Kategorie",
    options=development_categories,
    format_func=lambda x: x["name"]
)

development_indicators = get_available_category_indicators(development_config, selected_development_category)

selected_development = st.sidebar.selectbox(
    "Entwicklungsindikator",
    options=development_indicators,
    format_func=lambda x: x["short_description"]
)


st.write(
    "Auswahl:",
    selected_development
)