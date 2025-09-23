#!/bin/bash
# Script pour ajouter, committer et pousser sur la branche DEV

# Aller sur dev (la créer si elle n'existe pas encore)
git checkout dev 2>/dev/null || git checkout -b dev

# Ajouter tous les fichiers (hors .gitignore)
git add .

# Commit avec message automatique si aucun n'est fourni
if [ -z "$1" ]; then
  msg="Update on dev ($(date '+%Y-%m-%d %H:%M:%S'))"
else
  msg="$1"
fi
git commit -m "$msg"

# Pousser sur GitHub
git push -u origin dev

