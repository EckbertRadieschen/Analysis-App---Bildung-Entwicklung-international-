def get_available_change_offsets(indicator_config: dict) -> list[str]:
    meta = indicator_config["meta_data"]
    return [str(offset) for offset in meta["change_offsets"]]


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

    indicators = indicator_config["indicators"]
    category = category_dict["key"]

    indicator_list = [
        indicator
        for indicator in indicators.values()
        if indicator["category"] == category
    ]

    return sorted(
        indicator_list,
        key=lambda x: x["short_description"]
    )