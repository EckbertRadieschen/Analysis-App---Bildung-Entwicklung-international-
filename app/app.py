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


development_config = load_config(DEVELOPMENT_CONFIG)
education_config = load_config(EDUCATION_CONFIG)

st.title("Bildung und Länderentwicklung")

st.sidebar.header("Auswahl")

selected_development = st.sidebar.selectbox(
    "Entwicklungsindikator",
    development_config["indicators"].keys()
)


st.write(
    "Auswahl:",
    selected_development
)