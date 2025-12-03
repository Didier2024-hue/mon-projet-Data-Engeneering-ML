#!/bin/bash
set -euo pipefail

# ============================================================
# COLORS
# ============================================================
GREEN="\e[32m"
BLUE="\e[34m"
YELLOW="\e[33m"
RED="\e[31m"
NC="\e[0m"

# ============================================================
# DIRECTORIES
# ============================================================
SCRIPT_DIR="/home/datascientest/cde/scripts"

TARGETS=(
    "$SCRIPT_DIR/app"
    "$SCRIPT_DIR/db"
    "$SCRIPT_DIR/insert"
    "$SCRIPT_DIR/models"
    "$SCRIPT_DIR/preprocess"
    "$SCRIPT_DIR/scraping"
)

IGNORE="E302,E305,E402,E501,W293,W391,F401,F841,E704,E241,W291,E226,E303,E722,E128,E231,F541,W292,E741"

# ============================================================
# STORAGE
# ============================================================
declare -A ERRORS_PER_DIR=()
declare -A ERRORS_PER_CODE=()

TOTAL_ERRORS=0

# ============================================================
# PROCESS EACH DIRECTORY
# ============================================================
echo -e "${YELLOW}=== Lancement du Linting (avec statistiques) ===${NC}"

for dir in "${TARGETS[@]}"; do
    echo -e "\n${BLUE}→ Analyse : $dir${NC}"

    # Empêcher l'exit du script si flake8 renvoie des erreurs
    OUTPUT=$(flake8 "$dir" --max-line-length=200 --ignore="$IGNORE" 2>&1 || true)

    if [[ -z "$OUTPUT" ]]; then
        ERRORS_PER_DIR["$dir"]=0
        echo -e "${GREEN}  ✔ Aucun problème${NC}"
    else
        COUNT=$(echo "$OUTPUT" | wc -l)
        ERRORS_PER_DIR["$dir"]="$COUNT"
        TOTAL_ERRORS=$((TOTAL_ERRORS + COUNT))

        while IFS= read -r line; do
            # Sécurité : ignorer les lignes vides
            [[ -z "$line" ]] && continue

            # Extraire le code (ex: E501)
            CODE=$(echo "$line" | awk '{print $2}' | cut -d':' -f1 || true)

            # Ignorer si on n'a rien trouvé
            [[ -z "$CODE" ]] && continue

            # Incrémenter proprement
            ERRORS_PER_CODE["$CODE"]=$(( ${ERRORS_PER_CODE["$CODE"]:-0} + 1 ))
        done <<< "$OUTPUT"

        echo -e "${RED}  ✖ $COUNT erreurs rencontrées${NC}"
        echo "$OUTPUT"
    fi
done

# ============================================================
# REPORT (TABLE)
# ============================================================

echo -e "\n${YELLOW}=== Résumé des erreurs par répertoire ===${NC}"
printf "%-45s | %-10s\n" "Répertoire" "Erreurs"
printf -- "---------------------------------------------------------------\n"
for dir in "${TARGETS[@]}"; do
    printf "%-45s | %-10s\n" "$dir" "${ERRORS_PER_DIR["$dir"]}"
done

echo -e "\n${YELLOW}=== Résumé des erreurs par type ===${NC}"
printf "%-10s | %-10s\n" "Code" "Occurrences"
printf -- "---------------------------\n"
for code in "${!ERRORS_PER_CODE[@]}"; do
    printf "%-10s | %-10s\n" "$code" "${ERRORS_PER_CODE["$code"]}"
done

echo -e "\n${YELLOW}=== Total erreurs ===${NC}"
echo -e "${RED}${TOTAL_ERRORS} erreurs au total${NC}"

# ============================================================
# EXIT IF ERRORS
# ============================================================
if [[ $TOTAL_ERRORS -gt 0 ]]; then
    echo -e "${RED}✖ Le lint a détecté des erreurs${NC}"
    exit 1
fi

echo -e "${GREEN}✔ Aucun problème détecté — Lint OK${NC}"
