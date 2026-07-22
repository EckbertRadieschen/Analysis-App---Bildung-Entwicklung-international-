import streamlit as st
from buttons import choose_analytics_tool, choose_statistics_page

def navigation_content():
    with st.container(key="navigation_container"):

        navi_left, navi_right = st.columns([1, 0.8])

        with navi_left:
            st.markdown(
                """
                <div class="wrapper-title">
                    Navigation
                </div>
                """,
                unsafe_allow_html=True
            )

        with navi_right:
            navi_col1, navi_col2 = st.columns(2)

            with navi_col1:
                st.button(
                    "Analyse-Tool",
                    type=(
                        "primary"
                        if st.session_state.get("navigation_choice", "Analyse-Tool") == "Analyse-Tool"
                        else "secondary"
                    ),
                    use_container_width="stretch",
                    on_click=choose_analytics_tool
                )

            with navi_col2:
                st.button(
                    "Statistik-Seite",
                    type=(
                        "primary"
                        if st.session_state.get("navigation_choice", "Analyse-Tool") == "Statistik-Seite"
                        else "secondary"
                    ),
                    use_container_width="stretch",
                    on_click=choose_statistics_page
                )