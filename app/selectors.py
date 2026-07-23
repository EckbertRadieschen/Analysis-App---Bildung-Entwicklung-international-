import streamlit as st
import pandas as pd


# ===================================================================================================
# Selector Konfiguration
# ===================================================================================================

# ===================================================================================================
# Auswahl der Entwicklungskategorien
# ===================================================================================================

def get_available_development_categories(config: dict) -> list[dict]:
    """
        Gibt alle Entwicklungs-Kategorien zurück.
        Sortierung erfolgt nach Namen.
        """
    return sorted(
        config["meta_data"]["categories"],
        key=lambda x: x["name"]
    )


# ===================================================================================================
# Auswahl der Entwicklungsindikatoren
# ===================================================================================================

def get_available_development_category_indicators(indicator_config: dict, category_dict: dict) -> list[dict]:
    """
    Gibt alle Indikatoren einer Entwicklungs-Kategorie zurück.
    Sortierung erfolgt nach der Kurzbeschreibung.
    """
    if not category_dict:
        return []

    indicators = indicator_config["indicators"]
    category = category_dict["category"]

    indicator_list = [
        {
            "name": indicator["short_description"],
            "key": key
        }
        for key, indicator in indicators.items()
        if indicator["category"] == category
    ]

    return sorted(
        indicator_list,
        key=lambda indicator: indicator["name"]
    )

# ===================================================================================================
# Auswahl der Bildungskategorien
# ===================================================================================================

def get_available_education_categories(
    indicator_config: dict,
    change_offset: int,
    min_available_countries: int
) -> list[dict]:
    """
    Gibt nur Bildungskategorien zurück, in denen mindestens ein
    Bildungsindikator für den gewählten Offset ausreichend Daten besitzt.
    """

    categories = indicator_config["meta_data"]["categories"]
    indicators = indicator_config["indicators"]

    available_categories = []

    for category in categories:

        category_key = category["category"]

        has_available_indicator = False

        for indicator in indicators.values():

            if indicator["category"] != category_key:
                continue

            offset_data = indicator.get(
                "education_years",
                {}
            ).get(
                str(change_offset)
            )

            if (
                offset_data
                and offset_data["year"] is not None
                and offset_data["records"] >= min_available_countries
            ):
                has_available_indicator = True
                break

        if has_available_indicator:
            available_categories.append(category)

    return sorted(
        available_categories,
        key=lambda x: x["name"]
    )



# ==============================================================================================
# Wählt nur jene Bildungsindikatoren aus, die über ausreichend Werte verfügen
# ==============================================================================================

def get_available_education_indicators(
    indicator_config: dict,
    category_dict: dict,
    change_offset: int,
    min_available_countries: int
) -> list[dict]:
    """
    Gibt alle Bildungsindikatoren einer Kategorie zurück,
    die für den gewählten Change-Offset ausreichend Länderwerte besitzen.

    Rückgabe: [{"name": "...", "key": "..."}, ...]
    """

    if not category_dict:
        return []

    indicators = indicator_config["indicators"]
    category = category_dict["category"]

    indicator_list = []

    for indicator_code, indicator in indicators.items():

        if indicator["category"] != category:
            continue

        offset_data = (
            indicator
            .get("education_years", {})
            .get(str(change_offset))
        )

        if (
            offset_data is not None
            and offset_data["year"] is not None
            and offset_data["records"] >= min_available_countries
        ):
            indicator_list.append(
                {
                    "name": indicator["short_description"],
                    "key": indicator_code
                }
            )

    return sorted(
        indicator_list,
        key=lambda indicator: indicator["name"]
    )

# ==============================================================================================
# Gibt eine Liste mit allen Config-Offset-Werten aus
# ==============================================================================================


def get_change_offset_options(indicator_config: dict) -> list[int]:
    """
        Gibt alle in der Konfiguration hinterlegten Offset-Werte für 
        die Vergleichszeiträume zurück
        """
    meta = indicator_config.get("meta_data", {})
    
    return meta.get("change_offsets", [])



# ====================================================================
# Überprüft Vollständigkeit der Sidebar-Selector Eingaben
# ====================================================================    

def all_sidebar_selected ():
    selectors = [
        st.session_state.get("selected_development_category", None),
        st.session_state.get("selected_development_indicator", None),
        st.session_state.get("selected_education_category", None),
        st.session_state.get("selected_education_indicator", None),
        st.session_state.get("selected_change_offset", None)
    ]

    if all(selector is not None for selector in selectors):
        st.session_state["are_all_sidebar_selectors"] = True  
    else:
        st.session_state["are_all_sidebar_selectors"] = False


# ================================================================================================================================
# Wählt nur jene Bildungskategorien aus, die für die Correlations-Results relevant sind
# ================================================================================================================================

def get_available_statistics_categories(correlation_results: pd.DataFrame, category_type: str) -> list[str]:
    """
    Gibt alle vorhandenen Kategorien eines Typs zurück.
    """

    if category_type == "development":
        column = "development_category"

    elif category_type == "education":
        column = "education_category"

    else:
        raise ValueError(
            "category_type muss 'development' oder 'education' sein"
        )

    return sorted(
        correlation_results[column]
        .dropna()
        .unique()
        .tolist()
    )


# ================================================================================================================================
# Wählt nur jene Entwicklungskategorien aus, die für die Correlations-Results relevant sind
# ================================================================================================================================

def get_statistics_category_options(category_type: str) -> list[str]:
    """
    Liefert Kategorien sortiert nach Bewertung. Die stärkste Kategorie steht oben.
    """

    df = st.session_state["category_statistics"]

    df = df[df["category_type"] == category_type].copy()

    evaluation = st.session_state["selected_statistics_evaluation"]

    if evaluation == "Anzahl Zusammenhänge":
        sort_column = "count"
    else:
        sort_column = "median_abs_r"


    df = df.sort_values(sort_column,ascending=False)

    return df["category"].tolist()