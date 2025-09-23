#!/bin/bash

# -------------------------------
# Charger les variables depuis le .env.api
# -------------------------------
ENV_FILE="/home/datascientest/cde/.env.api"
if [ -f "$ENV_FILE" ]; then
    echo "🔹 Chargement des variables depuis $ENV_FILE"
    # shellcheck disable=SC1091
    source "$ENV_FILE"
else
    echo "❌ Fichier .env.api introuvable : $ENV_FILE"
    exit 1
fi

# Vérifier les variables essentielles
if [ -z "$BASE_DIR" ] || [ -z "$DATA_MODEL" ] || [ -z "$API_PORT" ]; then
    echo "❌ BASE_DIR, DATA_MODEL ou API_PORT non définis dans le .env.api"
    exit 1
fi

API_BASE="http://${API_HOST}:${API_PORT}"
EXPORT_DIR="./exports_$(date +%Y%m%d_%H%M%S)"
COMMENT="Ceci est un test de commentaire"

echo "🚀 Test API Trustpilot"

# -------------------------------
# 1️⃣ Test /health
# -------------------------------
echo "🔹 Test /health"
resp=$(curl -s "$API_BASE/health")
if [ -z "$resp" ]; then
    echo "⚠️ Pas de réponse de l'API"
else
    echo "$resp"
fi
echo "---------------------------------------------------"

# -------------------------------
# 2️⃣ Test /societes
# -------------------------------
echo "🔹 Test /societes"
resp=$(curl -s "$API_BASE/societes/?limit=100")
societes=$(echo "$resp" | jq -r '.societes[]?.nom // empty' | sed '/^$/d')
count=$(echo "$societes" | grep -c '.')
if [ "$count" -gt 0 ]; then
    echo "Sociétés trouvées ($count) :"
    echo "$societes"
else
    echo "⚠️ Pas de sociétés trouvées"
    societes=""
fi
echo "---------------------------------------------------"

# -------------------------------
# 3️⃣ Test /commentaires par société (1 commentaire chacun)
# -------------------------------
if [ "$count" -gt 0 ]; then
    for s in $societes; do
        id=$(echo "$s" | sed -E 's/\.(com|fr|net)$//')
        echo "🔹 Test /commentaires?societe=$id (1 commentaire)"
        resp=$(curl -s "$API_BASE/commentaires/?societe=$id&limit=1&page=1")
        count_com=$(echo "$resp" | jq '.commentaires? | length // 0' 2>/dev/null)
        count_com=${count_com:-0}
        if [ "$count_com" -gt 0 ]; then
            echo "$resp" | jq '.commentaires[:1]'
        else
            echo "⚠️ Pas de commentaires pour $id"
        fi
        echo "---------------------------------------------------"
    done
else
    echo "⚠️ Aucun commentaire car aucune société trouvée"
fi
echo "---------------------------------------------------"

# -------------------------------
# 4️⃣ Vérification des modèles pickle "linear*"
# -------------------------------
echo "🔹 Vérification des modèles pickle 'linear*' dans $DATA_MODEL"
linear_files=($(ls "$DATA_MODEL"/linear* 2>/dev/null))
if [ ${#linear_files[@]} -eq 0 ]; then
    echo "❌ Aucun fichier linear trouvé dans $DATA_MODEL"
else
    echo "✅ Modèles trouvés :"
    for f in "${linear_files[@]}"; do
        echo "   - $f"
    done
fi
echo "---------------------------------------------------"

# -------------------------------
# 5️⃣ Test /predict en POST
# -------------------------------
for type in note sentiment; do
    echo "🔹 Test POST /predict/$type"
    resp=$(curl -s -X POST "$API_BASE/predict/$type" \
        -H "Content-Type: application/json" \
        -d "{\"text\":\"$COMMENT\"}")
    echo "$type prediction : $resp"
done
echo "---------------------------------------------------"

# -------------------------------
# 6️⃣ Définir automatiquement SOC si non défini
# -------------------------------
if [ -z "$SOC" ]; then
    SOC=$(curl -s "$API_BASE/societes/?limit=1" | jq -r '.societes[0].nom')
    if [ -z "$SOC" ] || [ "$SOC" == "null" ]; then
        echo "❌ Impossible de récupérer une société pour l’export"
        exit 1
    else
        echo "🔹 Société utilisée pour l’export : $SOC"
    fi
fi
SOC_ID=$(echo "$SOC" | sed -E 's/\.(com|fr|net)$//')

# -------------------------------
# 7️⃣ Test /export/predictions
# -------------------------------
FORMATS="csv,json,xlsx"
LIMIT_EXPORT=3
echo "🔹 Test /export/predictions (limit=$LIMIT_EXPORT, formats=$FORMATS)"
resp=$(curl -s "$API_BASE/export/predictions?societe_id=$SOC_ID&limit=$LIMIT_EXPORT&formats=$FORMATS")
echo "Réponse export brute : $resp"

mkdir -p "$EXPORT_DIR"

files=$(echo "$resp" | jq -r '.files[]? // empty')
for f in $files; do
    if [ -f "$f" ]; then
        mv "$f" "$EXPORT_DIR/"
        echo "✅ Fichier déplacé : $EXPORT_DIR/$(basename $f)"
    else
        echo "❌ Fichier manquant : $f"
    fi
done
echo "---------------------------------------------------"

# -------------------------------
# 8️⃣ Smoke test GET dynamiques
# -------------------------------
echo "🔹 Smoke test GET sur tous les endpoints GET simples"

endpoints=$(docker exec -i fastapi-cde python - <<'PYTHON'
from api.main import app
for route in app.routes:
    if 'GET' in route.methods:
        print(route.path)
PYTHON
)

for ep in $endpoints; do
    # Ignorer /predict et /export qui nécessitent POST ou params
    if [[ "$ep" =~ ^/predict ]] || [[ "$ep" =~ ^/export ]]; then
        continue
    fi
    status=$(curl -s -o /dev/null -w "%{http_code}" "$API_BASE$ep")
    if [ "$status" -eq 200 ]; then
        echo "✅ $ep : OK"
    else
        echo "❌ $ep : KO (HTTP $status)"
    fi
done
echo "---------------------------------------------------"

echo "🎯 Test API complet terminé"
