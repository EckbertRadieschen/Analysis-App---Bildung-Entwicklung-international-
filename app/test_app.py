import streamlit as st

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    st.write("Sidebar Test")

st.write("Hauptinhalt")