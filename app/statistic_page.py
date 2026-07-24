import pandas as pd
import streamlit as st

from app.statistics_sidebar import statistics_sidebar_content
from app.statistics_overview import statistics_overview_content


def statistic_page():        
    statistics_sidebar_content()
    statistics_overview_content()