import streamlit as st
import pandas as pd
import plotly.express as px
from .api_client import get_societes_with_notes, get_last_comments, get_all_comments


def app():
    st.header("📈 Dashboard - Notes Globales des Sociétés")

    # =====================================
    # 🔍 Récupération des sociétés
    # =====================================
    societes_data = get_societes_with_notes()

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

    # Sélecteur de société
    societes_dict = {soc["nom"]: soc.get("id", soc["nom"]) for soc in societes_list if "nom" in soc}
    selected_societe_nom = st.selectbox("Choisissez une société", list(societes_dict.keys()))

    # Informations sur la société sélectionnée
    societe_data = next((s for s in societes_list if s["nom"] == selected_societe_nom), None)
    if not societe_data:
        st.error("Impossible de charger les données de cette société.")
        return

    # =====================================
    # 📊 Indicateurs principaux
    # =====================================
    col1, col2 = st.columns(2)
    with col1:
        note = societe_data.get("note_globale")
        st.metric("Note moyenne", f"{note:.2f}" if isinstance(note, (int, float)) else "N/A")
    with col2:
        total_avis = societe_data.get("total_avis") or societe_data.get("nombre_avis") or 0
        st.metric("Nombre total d'avis", total_avis)

    # =====================================
    # 🏢 Informations sur la société
    # =====================================
    st.subheader("Informations sur la société")
    df = pd.DataFrame([societe_data])
    cols_to_show = [c for c in ["nom", "note_globale", "total_avis", "nombre_avis"] if c in df.columns]
    if not df.empty and cols_to_show:
        st.dataframe(df[cols_to_show])
    else:
        st.info("Aucune donnée détaillée disponible pour cette société.")

    # =====================================
    # 📈 Analyse visuelle des notes
    # =====================================
    st.subheader("📈 Analyse visuelle des notes")

    # 💡 Nouveau : bascule entre les données "complètes" et "dernières"
    use_full = st.checkbox("Afficher tout l'historique", value=True)

    if use_full:
        comments = get_all_comments(societe_id=societe_data.get("nom"))
    else:
        comments = get_last_comments(societe_id=societe_data.get("nom"), limit=2000)

    # Vérification d’authentification
    if isinstance(comments, dict) and comments.get("error") == "auth_required":
        st.warning("🔐 Connectez-vous pour voir les graphiques et les commentaires.")
        st.stop()

    if comments and "comments" in comments and comments["comments"]:
        df_comments = pd.DataFrame(comments["comments"])

        if not df_comments.empty and "note_commentaire" in df_comments.columns:
            # Nettoyage et typage des données
            df_comments["note_commentaire"] = pd.to_numeric(df_comments["note_commentaire"], errors="coerce")
            df_comments["date"] = pd.to_datetime(df_comments.get("date"), errors="coerce")
            df_comments = df_comments.dropna(subset=["note_commentaire", "date"])
            df_comments = df_comments.sort_values("date")

            if not df_comments.empty:
                # 1️⃣ Agrégation mensuelle
                df_comments["annee_mois"] = df_comments["date"].dt.to_period("M")
                df_monthly = (
                    df_comments.groupby("annee_mois")["note_commentaire"]
                    .mean()
                    .reset_index()
                )
                df_monthly["date"] = df_monthly["annee_mois"].dt.to_timestamp()

                # 2️⃣ Série complète et interpolation
                full_range = pd.period_range(
                    df_monthly["annee_mois"].min(),
                    df_monthly["annee_mois"].max(),
                    freq="M"
                )
                df_monthly = (
                    df_monthly.set_index("annee_mois")
                    .reindex(full_range)
                    .rename_axis("annee_mois")
                    .reset_index()
                )
                df_monthly["date"] = df_monthly["annee_mois"].dt.to_timestamp()
                df_monthly["note_commentaire"] = df_monthly["note_commentaire"].interpolate(method="linear")

                # 3️⃣ Lissage visuel
                df_monthly["note_commentaire_smooth"] = (
                    df_monthly["note_commentaire"].rolling(window=3, min_periods=1).mean()
                )

                # 4️⃣ Graphique linéaire
                fig_line = px.line(
                    df_monthly,
                    x="date",
                    y="note_commentaire_smooth",
                    title=f"Évolution de la note moyenne - {selected_societe_nom}",
                    markers=True,
                )
                fig_line.update_layout(
                    yaxis_title="Note moyenne",
                    xaxis_title="Date",
                    height=400,
                    template="plotly_white",
                )
                st.plotly_chart(fig_line, use_container_width=True)

                # 5️⃣ Distribution
                fig_hist = px.histogram(
                    df_comments,
                    x="note_commentaire",
                    nbins=5,
                    title="Distribution des notes",
                    color_discrete_sequence=["#1f77b4"],
                )
                fig_hist.update_layout(
                    yaxis_title="Nombre d'avis",
                    xaxis_title="Note",
                    height=350,
                    template="plotly_white",
                )
                st.plotly_chart(fig_hist, use_container_width=True)

            else:
                st.info("Aucune donnée exploitable pour afficher les graphiques.")
        else:
            st.info("Pas de notes exploitables pour afficher des graphiques.")
    else:
        st.info("Aucun commentaire trouvé pour cette société.")

    # =====================================
    # 💬 Derniers commentaires récents
    # =====================================
    st.subheader("💬 Derniers commentaires récents")

    if comments and "comments" in comments and comments["comments"]:
        for comment in comments["comments"][:5]:
            with st.expander(f"Commentaire de {comment.get('auteur', 'Inconnu')}"):
                st.write(f"**Note :** {comment.get('note_commentaire', 'N/A')}")
                st.write(f"**Date :** {comment.get('date', 'N/A')}")
                st.write(f"**Commentaire :** {comment.get('commentaire', 'Aucun commentaire')}")
    else:
        st.info("Aucun commentaire récent.")
