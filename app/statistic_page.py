import pandas as pd
import streamlit as st

from app.statistics_sidebar import statistics_sidebar_content
from app.statistics_overview import statistics_overview_content
from app.statistics_details import statistics_details_content


def statistic_page():   

    selected_view = st.session_state.get("selected_statistics_view", "Gesamtübersicht")

    statistics_sidebar_content()

    if selected_view == "Gesamtübersicht": 
        statistics_overview_content()
    else: 
        statistics_details_content()