#!/bin/bash
# =====================================================
# 🔄 Script Git : push complet et sécurisé sur la branche DEV
# =====================================================

set -e  # Stoppe immédiatement si une erreur survient

# 1️⃣ Aller sur la branche dev (la créer si elle n'existe pas)
git checkout dev 2>/dev/null || git checkout -b dev

# 2️⃣ Vérifie la présence du .gitignore
if [ ! -f .gitignore ]; then
  echo "⚠️ Aucun .gitignore trouvé. Pense à en ajouter un pour éviter les gros fichiers et caches."
else
  echo "✅ .gitignore détecté — les fichiers ignorés seront exclus automatiquement."
fi

# 3️⃣ Nettoyage du cache Git des fichiers ignorés
echo "🧽 Nettoyage du cache Git..."
git rm -r --cached .vscode-server swapfile logs mlruns mlartifacts __pycache__ tmp cache data/tmp data/raw 2>/dev/null || true

# 4️⃣ Vérification des fichiers lourds (>100 Mo)
echo "⚖️ Vérification des fichiers lourds..."
large_files=$(find . -type f -size +100M | grep -v ".git/")
if [ -n "$large_files" ]; then
  echo "🚫 Ces fichiers dépassent 100 Mo et seront ignorés :"
  echo "$large_files"
  for f in $large_files; do
    echo "$f" >> .gitignore
    git rm --cached "$f" 2>/dev/null || true
  done
else
  echo "✅ Aucun fichier >100 Mo détecté."
fi

# 5️⃣ Ajout de tous les fichiers utiles
echo "📦 Ajout de tous les fichiers du projet..."
git add -A

# 6️⃣ Commit
if [ -z "$1" ]; then
  msg="Full secured update on dev ($(date '+%Y-%m-%d %H:%M:%S'))"
else
  msg="$1"
fi

git commit -m "$msg" || echo "ℹ️ Aucun changement à committer."

# 7️⃣ Push forcé vers la branche dev
echo "⬆️  Envoi sur la branche 'dev'..."
git push origin dev --force

echo "✅ Push complet et sécurisé effectué avec succès sur 'dev'."
