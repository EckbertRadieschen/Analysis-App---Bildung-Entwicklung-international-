import streamlit as st

def apply_markdown():
    st.markdown("""
        <style>
    /* Sidebar */
        section[data-testid="stSidebar"] {
            width: 400px !important
        }

        section[data-testid="stSidebar"] > div {
            width: 400px !important
        }

        section[data-testid="stSidebar"][aria-expanded="false"] {
            width: 0px !important;
            margin-left: 0px !important;
        }

        section[data-testid="stSidebar"][aria-expanded="false"] > div {
            width: 0px !important;
        }

    /* Divider */
        div[data-testid="stMarkdown"] hr {
            margin-top: 0.25rem;
            margin-bottom: 0.25rem
        }

    /* Selectbox Container */
        div[data-testid="stSelectbox"] div.react-aria-ComboBox > div {
            min-height: 25px;
            height: 25px
        }

    /* Text in der Selectbox */
        div[data-testid="stSelectbox"] input {
            font-size: 0.65rem
        }

    /* Dropdown-Pfeil */
        div[data-testid="stSelectbox"] button svg {
            height: 1rem;
            width: 1rem
        }

    /* Dropdown */
        div[role="listbox"] {
            max-height: 120px !important;
            font-size: 0.65rem;
            padding-top: 8px !important
        }

    /* Einträge im Dropdown */
        div[role="option"] {
            font-size: 0.65rem;
            height: 20px !important
        }
    </style>
    """, unsafe_allow_html=True)
