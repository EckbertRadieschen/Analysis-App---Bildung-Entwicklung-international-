import streamlit as st

def apply_markdown():
    st.markdown("""
        <style>
        /* Divider Höhe */
            div[data-testid="stMarkdown"] hr {
                margin-top: 0.25rem;
                margin-bottom: 0.25rem;
            }

    /* Selectbox Container kompakter machen */
        div[data-testid="stSelectbox"] div.react-aria-ComboBox > div {
            min-height: 25px;
            height: 25px;
        }

    /* Text in der Selectbox */
        div[data-testid="stSelectbox"] input {
            font-size: 0.65rem;
        }

    /* Dropdown-Pfeil */
            div[data-testid="stSelectbox"] button svg {
                height: 1rem;
                width: 1rem;
            }

    /* Schriftgröße im geöffneten Dropdown */
        div[role="listbox"] {
            font-size: 0.65rem;
        }

    /* Einträge im Dropdown */
        div[role="option"] {
            font-size: 0.65rem;
        }
        </style>
    """, unsafe_allow_html=True)
