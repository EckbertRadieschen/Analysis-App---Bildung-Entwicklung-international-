import streamlit as st


# ===================================================================================================
# Selector Konfiguration
# ===================================================================================================

def get_available_categories(config: dict) -> list[dict]:
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
        indicator
        for indicator in indicators.values()
        if indicator["category"] == category
    ]

    return sorted(
        indicator_list,
        key=lambda x: x["short_description"]
    )

def get_change_offset_options(indicator_config: dict):
    meta = indicator_config.get("meta_data", {})
    
    return meta.get("change_offsets", [])

def get_available_categories(config: dict) -> list[dict]:
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
        indicator
        for indicator in indicators.values()
        if indicator["category"] == category
    ]

    return sorted(
        indicator_list,
        key=lambda x: x["short_description"]
    )