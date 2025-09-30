# /home/datascientest/cde/api/scripts/pages/Prediction.py
import streamlit as st
from .api_client import predict_note, predict_sentiment

def app():
    st.header("🤖 Prédiction des Avis Trustpilot")

    text_input = st.text_area("Entrez un texte à analyser", height=150,
                              placeholder="Saisissez ici le texte dont vous voulez analyser le sentiment...")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Prédire la note"):
            if text_input.strip():
                with st.spinner("Analyse en cours..."):
                    result = predict_note(text_input)

                    # 🔐 Gestion auth
                    if isinstance(result, dict) and result.get("error") == "auth_required":
                        st.warning("🔐 Connectez-vous pour utiliser la prédiction.")
                        st.stop()

                    if "error" not in result:
                        st.success("Prédiction terminée")
                        note = result.get('note', 'N/A')
                        st.metric("Note prédite", f"{note}/5")
                        if isinstance(note, (int, float)):
                            st.progress(note/5)
                    else:
                        st.error(result["error"])
            else:
                st.warning("Veuillez entrer un texte à analyser")

    with col2:
        if st.button("Prédire le sentiment"):
            if text_input.strip():
                with st.spinner("Analyse en cours..."):
                    result = predict_sentiment(text_input)

                    # 🔐 Gestion auth
                    if isinstance(result, dict) and result.get("error") == "auth_required":
                        st.warning("🔐 Connectez-vous pour utiliser la prédiction.")
                        st.stop()

                    if "error" not in result:
                        st.success("Prédiction terminée")
                        sentiment = result.get('sentiment', 'N/A')
                        st.metric("Sentiment prédit", sentiment)
                        if sentiment == "positif":
                            st.success("✅ Texte positif")
                        elif sentiment == "négatif":
                            st.error("❌ Texte négatif")
                    else:
                        st.error(result["error"])
            else:
                st.warning("Veuillez entrer un texte à analyser")

    with st.expander("Exemples de textes pour tester"):
        st.write("""
        - **Positif**: "Service client exceptionnel, livraison rapide et produit de grande qualité. Je recommande vivement!"
        - **Négatif**: "Très déçu par ce produit qui est tombé en panne après une semaine d'utilisation. Service client injoignable."
        - **Neutre**: "J'ai commandé ce produit il y a 3 jours. La livraison était dans les temps. Rien à signaler."
        """)
