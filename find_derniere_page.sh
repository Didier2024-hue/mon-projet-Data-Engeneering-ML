#!/bin/bash

# Script pour trouver et afficher le contenu de derniere_page.txt
# uniquement dans /home/datascientest/cde/data/trustpilot

SEARCH_DIR="/home/datascientest/cde/data/trustpilot"

echo "Recherche des fichiers derniere_page.txt dans $SEARCH_DIR..."
echo ""

find "$SEARCH_DIR" -name "derniere_page.txt" -exec sh -c '
    echo "=========================================="
    echo "Fichier: $1"
    echo "Répertoire: $(dirname "$1")" 
    echo "Contenu:"
    cat "$1"
    echo ""
' sh {} \;

echo "Recherche terminée."
