# /home/datascientest/cde/api/scripts/pages/Exports.py
import streamlit as st
from .api_client import export_comments, get_societes_with_notes

def app():
    st.header("📤 Export de Données")
    
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
    
    n_comments = st.slider("Nombre de commentaires à exporter", min_value=10, max_value=200, value=50)
    
    formats = st.multiselect("Formats d'export", options=["csv", "json", "xlsx"], default=["csv"])
    
    if st.button("Exporter les données"):
        with st.spinner("Export en cours..."):
            result = export_comments(societe_id, n_comments, formats)
            
            if "error" not in result:
                st.success("Export terminé avec succès")
                
                # Afficher les informations sur les fichiers exportés
                if "files" in result:
                    st.write("Fichiers générés:")
                    for format_name, file_path in result["files"].items():
                        st.write(f"- {format_name.upper()}: {file_path}")
                else:
                    st.json(result)
            else:
                st.error(result["error"])