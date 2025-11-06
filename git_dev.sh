#!/bin/bash
# =====================================================
# 🔄 Script Git : push sur la branche DEV proprement
# =====================================================

# Aller sur dev (la créer si elle n'existe pas encore)
git checkout dev 2>/dev/null || git checkout -b dev

# Nettoyage des fichiers système à ignorer
echo "🧹 Nettoyage des fichiers temporaires..."
echo -e "\nswapfile\n.vscode-server/\n__pycache__/\n*.pyc\n.env\nlogs/\nmlruns/\n" >> .gitignore

# Supprime les fichiers non suivis indésirables du cache Git
git rm --cached -r swapfile .vscode-server/ 2>/dev/null

# Ajouter uniquement les fichiers utiles
git add api/ docker-compose.yml requirements.txt restart_compose.sh scripts/ data/ 2>/dev/null

# Message de commit
if [ -z "$1" ]; then
  msg="Update on dev ($(date '+%Y-%m-%d %H:%M:%S'))"
else
  msg="$1"
fi

# Commit + push
git commit -m "$msg"
git push origin dev --force

echo "✅ Push terminé sur la branche 'dev' avec succès."
