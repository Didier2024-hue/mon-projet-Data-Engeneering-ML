import streamlit as st
import pandas as pd
from .api_client import get_societes_with_notes, search_comments

def app():
    st.title("📤 Export de commentaires")

    # Sélection de la société
    societes_data = get_societes_with_notes().get("societes", [])
    societes = [s.get("societe") or s.get("nom") for s in societes_data if s]

    selected_societe = st.selectbox("Choisir une société :", societes)

    # Nombre de commentaires à récupérer
    n_commentaires = st.slider("Nombre de commentaires à récupérer :", 10, 500, 50)

    # Champ de recherche optionnel
    keyword = st.text_input("Filtrer les commentaires (mot-clé optionnel) :", "")

    if st.button("🔍 Rechercher les commentaires"):
        if keyword:
            data = search_comments(keyword, limit=n_commentaires)
        else:
            data = search_comments(selected_societe, limit=n_commentaires)

        if "results" in data and len(data["results"]) > 0:
            df = pd.DataFrame(data["results"])
            st.success(f"{len(df)} commentaires trouvés.")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="💾 Télécharger en CSV",
                data=csv,
                file_name=f"commentaires_{selected_societe}.csv",
                mime="text/csv",
            )
        else:
            st.warning("Aucun commentaire trouvé.")
