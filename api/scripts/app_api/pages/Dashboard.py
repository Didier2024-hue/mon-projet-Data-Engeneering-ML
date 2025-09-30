# /home/datascientest/cde/api/scripts/pages/Dashboard.py
import streamlit as st
import pandas as pd
from .api_client import get_societes_with_notes, get_last_comments

def app():
    st.header("📈 Dashboard - Notes Globales des Sociétés")

    # Récupérer la liste des sociétés
    societes_data = get_societes_with_notes()

    # 🔐 Gestion auth
    if isinstance(societes_data, dict) and societes_data.get("error") == "auth_required":
        st.warning("🔐 Cette page nécessite une connexion. Utilisez le formulaire de la barre latérale.")
        st.stop()

    if not societes_data or "societes" not in societes_data:
        st.info("Aucune société trouvée")
        return

    societes_list = societes_data["societes"]
    if not societes_list:
        st.warning("La liste des sociétés est vide")
        return

    # Menu pour choisir une société
    societes_dict = {soc["nom"]: soc.get("id", soc["nom"]) for soc in societes_list if "nom" in soc}
    selected_societe_nom = st.selectbox("Choisissez une société", list(societes_dict.keys()))

    # Récupérer les infos de la société sélectionnée
    societe_data = next((s for s in societes_list if s["nom"] == selected_societe_nom), None)
    if not societe_data:
        st.error("Impossible de charger les données de cette société")
        return

    # Affichage des métriques
    col1, col2 = st.columns(2)
    with col1:
        note = societe_data.get("note_globale")
        st.metric("Note moyenne", f"{note:.2f}" if isinstance(note, (int, float)) else "N/A")
    with col2:
        total_avis = societe_data.get("total_avis") or societe_data.get("nombre_avis") or 0
        st.metric("Nombre total d'avis", total_avis)

    # Détails
    st.subheader("Informations sur la société")
    df = pd.DataFrame([societe_data])
    cols_to_show = [c for c in ["nom", "note_globale", "total_avis", "nombre_avis"] if c in df.columns]
    if not df.empty and cols_to_show:
        st.dataframe(df[cols_to_show])
    else:
        st.info("Aucune donnée détaillée disponible pour cette société.")

    # Derniers commentaires
    st.subheader("Derniers commentaires")
    comments = get_last_comments(societe_id=societe_data.get("nom"), limit=5)

    # 🔐 Gestion auth
    if isinstance(comments, dict) and comments.get("error") == "auth_required":
        st.warning("🔐 Connectez-vous pour voir les derniers commentaires.")
        st.stop()

    if comments and "comments" in comments and comments["comments"]:
        for comment in comments["comments"]:
            with st.expander(f"Commentaire de {comment.get('auteur', 'Inconnu')}"):
                st.write(f"**Note:** {comment.get('note_commentaire', 'N/A')}")
                st.write(f"**Date:** {comment.get('date', 'N/A')}")
                st.write(f"**Commentaire:** {comment.get('commentaire', 'Aucun commentaire')}")
    else:
        st.info("Aucun commentaire récent")
