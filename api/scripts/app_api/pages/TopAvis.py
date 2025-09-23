# /home/datascientest/cde/api/scripts/pages/TopAvis.py
import streamlit as st
from .api_client import get_top_avis, get_societes_with_notes

def app():
    st.header("⭐ Avis les Plus Positifs et Négatifs")
    
    # Récupérer la liste des sociétés
    societes_data = get_societes_with_notes()
    if societes_data and 'societes' in societes_data:
        societes_list = societes_data['societes']
        societes_dict = {soc['nom']: soc.get('id', soc['nom']) for soc in societes_list if 'nom' in soc}
    else:
        societes_dict = {}
        st.error("Impossible de charger la liste des entreprises")
        return
    
    selected_societe = st.selectbox("Choisissez une entreprise", options=list(societes_dict.keys()))
    societe_id = societes_dict[selected_societe]
    
    avis_type = st.radio("Type d'avis", ["Positifs (note = 5)", "Négatifs (note = 1)"])
    limit = st.slider("Nombre d'avis à afficher", min_value=1, max_value=20, value=5)
    
    if st.button("Charger les avis"):
        with st.spinner("Chargement des avis..."):
            positif = avis_type == "Positifs (note = 5)"
            avis = get_top_avis(societe_id, limit=limit, positif=positif)
            
            if avis and 'top_avis' in avis and len(avis['top_avis']) > 0:
                st.success(f"{len(avis['top_avis'])} avis {'positifs' if positif else 'négatifs'} chargés")
                
                for avis_item in avis['top_avis']:
                    with st.expander(f"Avis de {avis_item.get('auteur', 'Inconnu')} - Note: {avis_item.get('note', 'N/A')}"):
                        st.write(f"**Commentaire:** {avis_item.get('commentaire', 'Pas de commentaire')}")
                        st.write(f"**Date:** {avis_item.get('date', 'Inconnue')}")
                        st.write(f"**Société:** {avis_item.get('societe', 'Inconnue')}")
            else:
                st.warning("Aucun avis trouvé pour cette entreprise")