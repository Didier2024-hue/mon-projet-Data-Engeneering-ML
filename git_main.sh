#!/bin/bash
# Script pour pousser sur la branche MAIN (stable)

# Aller sur main (la créer si elle n'existe pas encore depuis origin)
git checkout main 2>/dev/null || git checkout -b main origin/main

# Fusionner les changements depuis dev
git merge dev

# Ajouter tous les fichiers (au cas où)
git add .

# Commit avec message automatique si aucun n'est fourni
if [ -z "$1" ]; then
  msg="Update on main ($(date '+%Y-%m-%d %H:%M:%S'))"
else
  msg="$1"
fi
git commit -m "$msg"

# Pousser sur GitHub
git push -u origin main

