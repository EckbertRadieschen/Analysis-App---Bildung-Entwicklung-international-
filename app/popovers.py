
import streamlit as st

from app.buttons import (
    choose_top, choose_bottom,
    choose_development, choose_education, choose_comparison 
)


def popovers_content():
    po_blank_1, po_top_bottom_column, po_blank_2, po_bar_source_column, po_blank_3 = st.columns([1, 2, 1, 2, 1])

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