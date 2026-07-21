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
from src.analysis import (
    create_analysis_frames
)

from src.visuals import choose_main_chart


from app.selectors import (
    get_available_development_categories,
    get_available_development_category_indicators,
    get_available_education_categories,
    get_available_education_indicators,
    get_change_offset_options,
    all_sidebar_selected   
)

from app.buttons import (
    choose_bottom, choose_top,
    choose_development, choose_education, choose_comparison
)

from app.app_content import set_main_chart_title

from utils.hilfsfunktionen import get_max_year_from_config

from app.markdown import apply_markdown

# =======================================================================================================
# =======================================================================================================

apply_markdown()

development_config = load_config(DEVELOPMENT_CONFIG)
education_config = load_config(EDUCATION_CONFIG)

development_meta = development_config["meta_data"]
education_meta = education_config["meta_data"]

development_indicators_from_config = development_config["indicators"]
education_indicators_from_config = education_config["indicators"]


dev_max_year = get_max_year_from_config(development_config)
edu_max_year = get_max_year_from_config(education_config)

all_sidebar_selected()


# ============================================================================================
# Sidebar
# ============================================================================================

st.sidebar.header("Auswahl")
st.sidebar.divider()

# ============================================================================================
# Development Selectors
# ============================================================================================

st.sidebar.markdown("#### Entwicklungsvariable")

development_categories = get_available_development_categories(development_config)

selected_development_category = st.sidebar.selectbox(
    "Kategorie",
    options=development_categories,
    index=None,
    placeholder="Bitte Kategorie auswählen",
    format_func=lambda x: x["name"],
    key="selected_development_category"
)

development_indicators = get_available_development_category_indicators(development_config, selected_development_category)

selected_development_indicator = st.sidebar.selectbox(
    "Indikator",
    options=development_indicators,
    index=None,
    placeholder=(
        "Bitte Indikator auswählen" 
        if selected_development_category is not None
        else "Bitte zunächst Kategorie auswählen"
    ),
    format_func=lambda x: x["name"],
    disabled=selected_development_category is None,
    key="selected_development_indicator"
)

change_offsets = get_change_offset_options(development_config)

selected_change_offset = st.sidebar.selectbox(
    "Vergleichszeitraum",
    options=change_offsets,
    index=None,
    placeholder="Bitte Zeitraum auswählen",
    format_func=lambda x: f"{x} Jahre",
    key="selected_change_offset"
)

# ============================================================================================
# Education Selectors
# ============================================================================================

st.sidebar.divider()

st.sidebar.markdown("#### Bildungsindikator")

education_categories = get_available_education_categories(
    education_config,
    selected_change_offset,
    education_meta["min_available_countries"]
)

selected_education_category = st.sidebar.selectbox(
    "Kategorie",
    options=education_categories,
    index=None,
    placeholder="Bitte Kategorie auswählen",
    format_func=lambda x: x["name"],
    key="selected_education_category"
)

education_indicators = get_available_education_indicators(
    education_config, 
    selected_education_category,
    selected_change_offset,
    education_meta["min_available_countries"]
)

selected_education_indicator = st.sidebar.selectbox(
    "Indikator",
    options=education_indicators,
    index=None,
    placeholder=(
        "Bitte Indikator auswählen" 
        if (
            selected_education_category is not None
            and selected_change_offset is not None
        )
        else "Bitte zunächst Kategorie und Vergleichszeitraum auswählen"
    ),
    format_func=lambda x: x["name"],
    disabled=(
        selected_education_category is None
        or selected_change_offset is None
    ),
    key="selected_education_indicator"
)




# ============================================================================================
# Hauptbereich - Popovers
# ============================================================================================

if st.session_state["are_all_sidebar_selectors"]:
    st.subheader(set_main_chart_title(education_config))

    po_top_bottom_column, blank_1, po_bar_source_column = st.columns([2, 1, 2])

    if st.session_state.get("main_bar_source_choice", "Entwicklungsvariable") in ["Entwicklungsvariable", "Bildungsindikator"]:
        with po_top_bottom_column:
            with st.popover(st.session_state.get("top_bottom_choice", "Top 10"), width="stretch"):
                st.button(
                    "Top 10",
                    type="primary" if st.session_state.get("top_bottom_choice", "Top 10") == "Top 10" else "secondary",
                    use_container_width="stretch",
                    on_click=choose_top
                )

                st.button(
                    "Bottom 10",
                    type="primary" if st.session_state.get("top_bottom_choice", "Top 10") == "Bottom 10" else "secondary",
                    use_container_width="stretch",
                    on_click=choose_bottom
                )

    with po_bar_source_column:
        with st.popover(st.session_state.get("main_bar_source_choice", "Entwicklungsvariable"), width="stretch"):
            st.button(
                "Enwicklungsvariable",
                type=(
                    "primary" 
                    if st.session_state.get("main_bar_source_choice", "Entwicklungsvariable") == "Entwicklungsvariable" 
                    else "secondary"
                ),
                use_container_width="stretch",
                on_click=choose_development
            )
    
            st.button(
                "Bildungsindikator",
                type=(
                    "primary" 
                    if st.session_state.get("main_bar_source_choice", "Entwicklungsvariable") == "Bildungsindikator" 
                    else "secondary"
                ),
                use_container_width="stretch",
                on_click=choose_education
            )

            st.button(
                "Zusammenhang",
                type=(
                    "primary" 
                    if st.session_state.get("main_bar_source_choice", "Entwicklungsvariable") == "Zusammenhang" 
                    else "secondary"
                ),
                use_container_width="stretch",
                on_click=choose_comparison
            )
else:
    st.title("Willkommen im Analyse-Tool")

st.divider()

# ============================================================================================
# Hauptbereich
# ============================================================================================

if st.session_state["are_all_sidebar_selectors"]:
    with st.spinner("Analysedaten werden erstellt..."):

        create_analysis_frames(
            selected_development_indicator,
            selected_education_indicator,
            development_config,
            education_config
        )

        fig = choose_main_chart()
        
        st.plotly_chart(fig)

else:
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
        Wählen Sie zur Analyse über die Sidebar eine beliebige Konfiguration<br>
        von Entwicklungs- und Bildungsindikatoren sowie einen Vergleichszeitraum,<br>
        über den der Entwicklungstrend berechnet werden soll.<br><br>
        Beachten Sie, dass je nach Vergleichszeitraum eine andere Auswahl<br>
        an Bildungsindikatoren verfügbar sein kann.
    """, unsafe_allow_html=True)

    

    





