import streamlit as st

def apply_markdown():
    st.markdown(
        """
        <style>
        /* Header der App */
            header[data-testid="stHeader"] {
                display: none
            }
        /* Main Container */
            [data-testid="stMainBlockContainer"] {
                padding: 0 !important;
                margin: 0 !important
            }

            [data-testid="stMainBlockContainer"] > div:first-child {
                margin-top: -1rem !important;
            }

    /* ==========================================================
    === Navigationsleiste
    ========================================================== */  
            
            .st-key-intro_container {
                width: 80%;
                border-radius: 0;
                margin: auto;
                margin-left: 12rem
            }

            .st-key-intro_container p,
            .st-key-intro_container li {
                font-size: 0.95rem;
                line-height: 1.6;
            }

            .st-key-intro_container h3 {
                font-size: 1.5rem;
            }

            .st-key-intro_container h4 {
                font-size: 1.2rem;
            }

    /* ==========================================================
    === Navigationsleiste
    ========================================================== */

            .st-key-navigation_container {
                height: 2rem;
                background-color: #faedce;
                padding: 0.8rem 3rem;
                margin-top: 0 !important;
                border-radius: 0;
                border-bottom: 1px solid;
                border-color: #a67b5b
            }

            .st-key-navigation_container div[data-testid="stElementContainer"]:has(div[data-testid="stButton"]) {
                height: 100%
            }

            .st-key-navigation_container div[data-testid="stButton"] button {
                height: 100% !important;
                min-height: 0 !important;
                padding: 0 !important
            }

            
    /* ==========================================================
    === Sidebar
    ========================================================== */
            
        /* Sidebar */

            .st-key-sidebar_title_container {
                background-color: #faedce;
                width: 100%;
                margin-top: 1rem !important;
                margin-bottom: 1.5rem;
                border-radius: 0
            }

            section[data-testid="stSidebar"] {
                width: 400px !important;
                border-right: 1px solid;
                border-color: #a67b5b
            }

            section[data-testid="stSidebar"] > div {
                width: 400px !important
            }

            [data-testid="stSidebarHeader"] {
                display: none !important
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

    /* ==========================================================
    === Hauptbereich Header
    ========================================================== */

        .custom-subheader {
            width: fit-content;
            margin: 0 auto;
            text-align: center;
        }

        .custom-title {
            font-size: 1.25rem;
            font-weight: 600;
            line-height: 1.3;
        }

        .custom-subtitle {
            font-size: 0.9rem;
            font-weight: 400;
            color: rgba(49, 51, 63, 0.7);
            margin-top: 0.2rem;
        }       

    /* ==========================================================
    === Stats Container
    ========================================================== */

        /* Stats Container */
            .stats-container {
                margin-top: 120px;
                padding: 16px 18px;
                border: 1px solid rgba(128, 128, 128, 0.3);
                border-radius: 0.5rem
            }
    
    /* ==========================================================
    === Textformate
    ========================================================== */

        /* Text- und Titelformate */
            .small-text {
                font-size: 13px;
                padding-bottom: 12px;
                margin-bottom: 15px
            }

            .medium-title {
                font-size: 16px;
                font-weight: 600
            }

            .wrapper-title {
                font-size: 1.1rem;
                font-weight: 700;
            }
        </style>
        """, unsafe_allow_html=True)
