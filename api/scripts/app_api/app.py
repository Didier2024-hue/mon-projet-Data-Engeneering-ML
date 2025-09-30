import streamlit as st
from pages import Dashboard, TopAvis, Prediction, Exports
from pages.api_client import login as api_login, logout as api_logout, set_token, is_authenticated

st.set_page_config(page_title="Trustpilot App", layout="wide")
st.title("📊 Application Trustpilot – via API")

# --- Auth UI (sidebar) ---
st.sidebar.markdown("### Authentification")

# Si tu conserves le token en session, réinjecte-le au démarrage
if "access_token" in st.session_state and st.session_state["access_token"]:
    set_token(st.session_state["access_token"])

if not is_authenticated():
    with st.sidebar.form("login_form", clear_on_submit=False):
        username = st.text_input("Utilisateur", key="user_input")
        password = st.text_input("Mot de passe", type="password", key="pwd_input")
        submitted = st.form_submit_button("Se connecter")
    if submitted:
        res = api_login(username, password)
        if isinstance(res, dict) and res.get("access_token"):
            st.session_state["access_token"] = res["access_token"]
            set_token(res["access_token"])
            st.sidebar.success("Connecté")
            st.rerun()
        else:
            st.sidebar.error(res.get("detail") or res.get("error") or "Échec de connexion")
else:
    st.sidebar.success("Connecté")
    if st.sidebar.button("🔒 Déconnexion", use_container_width=True):
        api_logout()
        st.session_state.pop("access_token", None)
        st.sidebar.info("Déconnecté")
        st.rerun()

st.sidebar.markdown("---")
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
