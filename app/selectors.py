import streamlit as st


# ===================================================================================================
# Selector Konfiguration
# ===================================================================================================

def get_available_categories(config: dict) -> list[dict]:
    """
        Gibt alle Kategorien zurück.
        Sortierung erfolgt nach Namen.
        """
    return sorted(
        config["meta_data"]["categories"],
        key=lambda x: x["name"]
    )


def get_available_category_indicators(indicator_config: dict, category_dict: dict) -> list[dict]:
    """
    Gibt alle Indikatoren einer Kategorie zurück.
    Sortierung erfolgt nach der Kurzbeschreibung.
    """
    if not category_dict:
        return []

    indicators = indicator_config["indicators"]
    category = category_dict["category"]

    indicator_list = [
        (key, indicator)
        for key, indicator in indicators.items()
        if indicator["category"] == category
    ]

    return sorted(
        indicator_list,
        key=lambda x: x[1]["short_description"]
    )


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