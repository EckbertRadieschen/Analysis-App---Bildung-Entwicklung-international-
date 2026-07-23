import pandas as pd
from src.preparations import load_config
from src.analysis import create_dev_change_columns, load_correlation_results
from utils.hilfsfunktionen import short_analysis_frame


from src.paths import (
    EDUCATION_RAW,
    DEVELOPMENT_CONFIG,
    EDUCATION_CONFIG,
    EDUCATION_OUTPUT,
    DEVELOPMENT_OUTPUT,
    CORRELATION_RESULTS,
    TEST_CORRELATION_RESULTS
)


correlation_results = load_config(CORRELATION_RESULTS)

df_correlation = load_correlation_results()

short_analysis_frame(df_correlation)

correlation_results_2 = load_config(TEST_CORRELATION_RESULTS)

df_correlation_2 = load_correlation_results()

short_analysis_frame(df_correlation)
