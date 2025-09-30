#!/bin/bash

# ===============================
# Config
# ===============================
ENV_FILE="/home/datascientest/cde/api/.env.api"
EXPORT_DIR="./exports_$(date +%Y%m%d_%H%M%S)"
COMMENT="Ceci est un test de commentaire"
MODEL_SCOPE="${MODEL_SCOPE:-linearsvc}"  # "linearsvc" (défaut) ou "all"

# ===============================
# Charger l'env
# ===============================
if [ -f "$ENV_FILE" ]; then
  echo "🔹 Chargement des variables depuis $ENV_FILE"
  # shellcheck disable=SC1091
  source "$ENV_FILE"
else
  echo "❌ Fichier .env.api introuvable : $ENV_FILE"
  exit 1
fi

if [ -z "$BASE_DIR" ] || [ -z "$DATA_MODEL" ] || [ -z "$API_PORT" ]; then
  echo "❌ BASE_DIR, DATA_MODEL ou API_PORT non définis dans le .env.api"
  exit 1
fi

# ===============================
# API_BASE avec fallback
# ===============================
if [ -n "$1" ]; then
  API_BASE="http://$1:${API_PORT}"
else
  API_BASE="http://${API_HOST}:${API_PORT}"
  if ! curl -s --max-time 2 "$API_BASE/health" >/dev/null; then
    HOST_IP=$(hostname -I | awk '{print $1}')
    API_BASE="http://${HOST_IP}:${API_PORT}"
  fi
fi
echo "🌍 API_BASE utilisé : $API_BASE"
echo "🚀 Test API Trustpilot"

# ===============================
# 1) /health
# ===============================
echo "🔹 Test /health"
resp=$(curl -s "$API_BASE/health")
if [ -z "$resp" ]; then
  echo "⚠️ Pas de réponse de l'API"
else
  echo "$resp"
fi
echo "---------------------------------------------------"

# ===============================
# 2) /societes
# ===============================
echo "🔹 Test /societes"
resp=$(curl -s "$API_BASE/societes/?limit=100")
societes=$(echo "$resp" | jq -r '.[]?.nom // empty' | sed '/^$/d')
count=$(echo "$societes" | grep -c '.' || echo 0)
if [ "$count" -gt 0 ]; then
  echo "Sociétés trouvées ($count) :"
  echo "$societes"
else
  echo "⚠️ Pas de sociétés trouvées"
  societes=""
fi
echo "---------------------------------------------------"

# ===============================
# 3) /commentaires (1 par société)
#    IMPORTANT: utiliser societe_id (sans .com/.fr/.net)
# ===============================
if [ "$count" -gt 0 ]; then
  while read -r s; do
    [ -z "$s" ] && continue
    id=$(echo "$s" | sed -E 's/\.(com|fr|net)$//')
    echo "🔹 Test /commentaires?societe_id=$id (1 commentaire)"
    resp=$(curl -s "$API_BASE/commentaires/?societe_id=$id&limit=1&page=1")

    # L'endpoint renvoie un ARRAY de commentaires (ex: [{...}, {...}])
    total=$(echo "$resp" | jq 'length' 2>/dev/null)
    total=${total:-0}

    if [ "$total" -gt 0 ]; then
      echo "✅ $total commentaire(s) trouvé(s) pour $id. Aperçu du 1er :"
      echo "$resp" | jq '.[0]'
    else
      echo "ℹ️ Aucun commentaire dispo pour $id (vérifie le mapping ou l’indexation)"
    fi
    echo "---------------------------------------------------"
  done <<< "$societes"
else
  echo "⚠️ Aucun commentaire car aucune société trouvée"
fi
echo "---------------------------------------------------"

# ===============================
# 4) Vérif des modèles pickle
# ===============================
if [ "$MODEL_SCOPE" = "all" ]; then
  echo "🔹 Vérification des modèles pickle (linear*, linearsvc*, logistic*, randomforest*) dans $DATA_MODEL"
  model_files=$(docker exec fastapi-cde sh -c "ls $DATA_MODEL/*{linear*,linearsvc*,logistic*,randomforest*} 2>/dev/null")
else
  echo "🔹 Vérification des modèles pickle (linearsvc*) dans $DATA_MODEL"
  model_files=$(docker exec fastapi-cde sh -c "ls $DATA_MODEL/linearsvc* 2>/dev/null")
fi

if [ -z "$model_files" ]; then
  echo "❌ Aucun fichier modèle correspondant trouvé dans $DATA_MODEL (scope: $MODEL_SCOPE)"
else
  echo "✅ Modèles trouvés :"
  echo "$model_files" | sed 's/^/   - /'
fi
echo "---------------------------------------------------"

# ===============================
# 5) /predict (POST)
# ===============================
for type in note sentiment; do
  echo "🔹 Test POST /predict/$type"
  resp=$(curl -s -X POST "$API_BASE/predict/$type" \
    -H "Content-Type: application/json" \
    -d "{\"commentaire\":\"$COMMENT\"}")
  echo "$type prediction : $resp"
done
echo "---------------------------------------------------"

# ===============================
# 6) Choix d'une société par défaut pour l'export
#    (on part du nom complet, puis id_societe = sans TLD)
# ===============================
if [ -z "$SOC" ]; then
  SOC=$(curl -s "$API_BASE/societes/?limit=1" | jq -r '.[0].nom')
  if [ -z "$SOC" ] || [ "$SOC" == "null" ]; then
    echo "❌ Impossible de récupérer une société pour l’export"
    exit 1
  else
    echo "🔹 Société utilisée pour l’export : $SOC"
  fi
fi
SOC_ID=$(echo "$SOC" | sed -E 's/\.(com|fr|net)$//')

# ===============================
# 7) /export (POST societe_id)
# ===============================
FORMATS="csv,json,xlsx"
LIMIT_EXPORT=3
echo "🔹 Test /export (POST societe_id=$SOC_ID, limit=$LIMIT_EXPORT, formats=$FORMATS)"
resp=$(curl -s -X POST "$API_BASE/export/" \
  -H "Content-Type: application/json" \
  -d "{\"societe_id\":\"$SOC_ID\", \"limit\":$LIMIT_EXPORT, \"formats\":\"$FORMATS\"}")
echo "Réponse export brute : $resp"

mkdir -p "$EXPORT_DIR"
files=$(echo "$resp" | jq -r '.files[]? // empty' 2>/dev/null)
for f in $files; do
  if [ -f "$f" ]; then
    mv "$f" "$EXPORT_DIR/"
    echo "✅ Fichier déplacé : $EXPORT_DIR/$(basename "$f")"
  else
    echo "❌ Fichier manquant : $f"
  fi
done
echo "---------------------------------------------------"

# ===============================
# 8) Smoke test GET via OpenAPI
# ===============================
echo "🔹 Smoke test GET via /openapi.json"
endpoints=$(curl -s "$API_BASE/openapi.json" | jq -r '.paths | keys[]')
for ep in $endpoints; do
  # Ignorer endpoints qui nécessitent POST ou auth
  if [[ "$ep" =~ ^/predict ]] || [[ "$ep" =~ ^/export ]] || [[ "$ep" =~ ^/auth ]]; then
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
