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
                height: 100%;
                background-color: #faedce;
                padding: 0.8rem 1rem;
                margin: 0 !important;
                border-radius: 0;
                border-bottom: 1px solid;
                border-color: #cccccc
            }

            .st-key-navigation_container div[data-testid="stElementContainer"]:has(div[data-testid="stButton"]) {
                height: 100%
            }

            .st-key-navigation_container div[data-testid="stButton"] button {
                height: 25px !important;
                min-height: 0 !important;
                padding: 0 !important
            }

            .st-key-navigation_container div[data-testid="stButton"] p {
                font-size: 12px !important
            }
            

    /* ==========================================================
    === Sidebar
    ========================================================== */
            
        /* Sidebar */

            .st-key-sidebar_title_container {
                background-color: #faedce;
                width: 100%;
                margin-bottom: 1.5rem;
                border-radius: 0
            }

            section[data-testid="stSidebar"] {
                width: 400px !important;
                border-right: 1px solid;
                border-color: #a67b5b;
                padding: 0 !important
            }

            [data-testid="stSidebarContent"] {
                padding: 0 10px
            }

            [data-testid="stSidebarContent"] > div {
                padding: 0 !important;
                margin: 0 !important;
            }

            [data-testid="stSidebarHeader"] {
                display: none !important
            }

            div[data-testid="stLayoutWrapper"]:has(.wrapper-title) {
                margin-top: 3px
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

        /* Radio-Buttons */    
            div[role="radiogroup"] p {
                font-size: 12px !important;
            }

    /* ==========================================================
    === Hauptbereich Header
    ========================================================== */

        .analytic-title {
            width: 100%;
            margin-top: 1rem;
            margin-bottom: 1px;
            font-size: 20px;
            font-weight: 600;
            text-align: center
        }

        .analytic-info {
            width: 70%;
            margin: auto;
            margin-top: 10rem;
            font-size: 16px
        }

        .custom-subheader {
            width: fit-content;
            margin: auto;
            margin-top: 0.5rem;
            text-align: center;
        }

        .custom-title {
            font-size: 1rem;
            font-weight: 600;
            line-height: 1.3;
        }

        .custom-subtitle {
            font-size: 0.7rem;
            font-weight: 400;
            color: rgba(49, 51, 63, 0.7);
            margin-top: 0.2rem;
        }      

        .custom-sub_subtitle {
            font-size: 0.5rem;
            font-weight: 400;
            color: rgba(49, 51, 63, 0.7);
            margin-top: 0.1rem;
        }   

        div[data-testid="stElementContainer"]:has(.stAlert) {
            margin-top: 5rem;
            padding: 1rem 2rem
        }

        div[data-testid="stAlertContainer"] {
            background-color: #faedce;
            font-size: 14px;
            display: flex;
            text-align: center
        }

        div[data-testid="stAlertContainer"] p {
            font-size: 14px
        }

    /* ==========================================================
    === PopOvers
    ========================================================== */    
        
        div[data-testid="stLayoutWrapper"]:has(div[data-testid="stPopover"]) {
            margin-top: 5px;
            margin-bottom: -7px
        }   

        div[data-testid="stPopover"] p {
            font-size: 12px
        }

        [data-testid="stPopover"] > div > button {
            height: 25px;
            min-height: 25px
        }

        [data-testid="stPopoverBody"] button p {
            font-size: 12px
        }

        [data-testid="stPopoverBody"] {
            padding: 10px 10px !important
        }

        [data-testid="stVerticalBlock"]:has(.st-key-top_10) {
            gap: 0.5rem
        }

        [data-testid="stVerticalBlock"]:has(.st-key-entwicklungsvariable) {
            gap: 0.5rem
        }

        [data-testid="stPopoverBody"] [data-testid="stButton"] > button {
            height: 25px;
            min-height: 25px;
            padding: 0;
            display: flex;
            align-items: center;
            justify-content: center;
        }

    /* ==========================================================
    === Hauptbereich
    ========================================================== */    

        .st-key-intro_container {
            margin: 4rem 7rem;
            height: 90%;
            width: 90%
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
                padding-bottom: 5px;
                margin-bottom: 5px
            }

            ol, ul, blockquote {
                font-size: 13px;
                margin-left: 20px !important
            }

            .medium-title {
                font-size: 16px;
                font-weight: 600
            }

            .chart-title {
                width: 100%;
                margin-top: 10px;
                font-size: 14px;
                font-weight: 800;
                text-align: center
            }

            .small-intro-text {
                font-size: 13px;
                padding-bottom: 5px;
                margin-top: 10px
            }

            .small-intro-text li {
                font-size: 13px;
            }

            .medium-intro-title {
                font-size: 16px;
                font-weight: 600
            }

            .wrapper-title {
                font-size: 1.1rem;
                font-weight: 700
            }

            .info-text {
                width: 85%;
                font-size: 10px;
                color: #666;
                line-height: 1.4;

                padding: 6px;
                padding-left: 20px;

                margin-top: 10px;
                margin-left: 50px;
                margin-bottom: 10px;

                background-color: #fdf7f2;
                border: 1px solid #e7c8aa;
                border-radius: 6px
            }
        </style>
        """, unsafe_allow_html=True)