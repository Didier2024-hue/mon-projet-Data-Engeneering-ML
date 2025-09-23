#!/bin/bash
# Script pour pousser sur la branche DEV (développement)
# ⚠️ Attention : cela écrase la branche dev distante avec le contenu local

# Aller sur dev (la créer si elle n'existe pas encore)
git checkout dev 2>/dev/null || git checkout -b dev

# Ajouter tous les fichiers
git add .

# Commit avec message automatique si aucun n'est fourni
if [ -z "$1" ]; then
  msg="Update on dev ($(date '+%Y-%m-%d %H:%M:%S'))"
else
  msg="$1"
fi
git commit -m "$msg"

# Pousser en forçant pour que le remote = local
git push origin dev --force

