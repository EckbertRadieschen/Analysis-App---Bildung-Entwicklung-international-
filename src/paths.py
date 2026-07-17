from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ==================================================================
# Directories
# ==================================================================

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

CONFIG_DIR = BASE_DIR / "config"

# ==================================================================
# Konfigurationsdateien
# ==================================================================

DEVELOPMENT_CONFIG = CONFIG_DIR / "development_indicators.json"
EDUCATION_CONFIG = CONFIG_DIR / "education_indicators.json"

# ==================================================================
# Datenquellen
# ==================================================================

DEVELOPMENT_RAW = RAW_DATA_DIR / "development_data.csv"
EDUCATION_RAW = RAW_DATA_DIR / "education_data.csv"
COUNTRY_INFO = RAW_DATA_DIR / "country_info.csv"

# ==================================================================
# Prozessierte Daten
# ==================================================================

DEVELOPMENT_OUTPUT = PROCESSED_DATA_DIR / "development_indicators.csv"
EDUCATION_OUTPUT = PROCESSED_DATA_DIR / "education_indicators.csv"