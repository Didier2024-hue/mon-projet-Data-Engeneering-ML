#!/bin/bash
# Script pour écraser la branche MAIN avec le contenu de DEV
# ⚠️ Attention : cela écrase complètement main distant avec dev local

# S'assurer qu'on est bien sur dev
git checkout dev

# Mettre à jour dev (au cas où)
git add .
if [ -z "$1" ]; then
  msg="Sync dev -> main ($(date '+%Y-%m-%d %H:%M:%S'))"
else
  msg="$1"
fi
git commit -m "$msg"

# Recréer main à partir de dev (localement)
git branch -D main 2>/dev/null || true
git checkout -b main

# Pousser en forçant main = dev
git push origin main --force

# Revenir sur dev pour continuer à bosser
git checkout dev

