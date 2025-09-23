import streamlit as st
from pages import Dashboard, TopAvis, Prediction, Exports

st.set_page_config(page_title="Trustpilot App", layout="wide")
st.title("📊 Application Trustpilot – via API")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à :", ["Dashboard", "Top Avis", "Prédiction", "Exports"])

if page == "Dashboard":
    Dashboard.app()
elif page == "Top Avis":
    TopAvis.app()
elif page == "Prédiction":
    Prediction.app()
elif page == "Exports":
    Exports.app()
