#!/bin/bash

OUTPUT="rapport_systeme.txt"

echo "======================================" > $OUTPUT
echo "   RAPPORT SYSTEME - ENVIRONNEMENT    " >> $OUTPUT
echo "======================================" >> $OUTPUT
echo "" >> $OUTPUT

# -------------------------------
# Version Ubuntu
# -------------------------------
echo "🔹 Version Ubuntu" >> $OUTPUT
lsb_release -a >> $OUTPUT 2>&1
echo "" >> $OUTPUT

# -------------------------------
# Kernel / Architecture
# -------------------------------
echo "🔹 Kernel & Architecture" >> $OUTPUT
uname -a >> $OUTPUT
echo "" >> $OUTPUT

# -------------------------------
# CPU / RAM
# -------------------------------
echo "🔹 CPU" >> $OUTPUT
lscpu >> $OUTPUT
echo "" >> $OUTPUT

echo "🔹 Mémoire (RAM)" >> $OUTPUT
free -h >> $OUTPUT
echo "" >> $OUTPUT

# -------------------------------
# Disque
# -------------------------------
echo "🔹 Espace disque" >> $OUTPUT
df -h >> $OUTPUT
echo "" >> $OUTPUT

# -------------------------------
# Python & Pip
# -------------------------------
echo "🔹 Versions Python & Pip" >> $OUTPUT
python3 --version >> $OUTPUT 2>&1
pip3 --version >> $OUTPUT 2>&1
echo "" >> $OUTPUT

echo "🔹 Packages Python installés" >> $OUTPUT
pip3 list >> $OUTPUT 2>&1
echo "" >> $OUTPUT

# -------------------------------
# OpenSSL
# -------------------------------
echo "🔹 Version OpenSSL" >> $OUTPUT
openssl version >> $OUTPUT 2>&1
echo "" >> $OUTPUT

# -------------------------------
# Docker
# -------------------------------
echo "🔹 Version Docker" >> $OUTPUT
docker --version >> $OUTPUT 2>&1
echo "" >> $OUTPUT

echo "🔹 Version Docker Compose" >> $OUTPUT
docker compose version >> $OUTPUT 2>&1
echo "" >> $OUTPUT

echo "🔹 Info Docker" >> $OUTPUT
docker info >> $OUTPUT 2>&1
echo "" >> $OUTPUT

# -------------------------------
# Réseau Docker
# -------------------------------
echo "🔹 Réseaux Docker" >> $OUTPUT
docker network ls >> $OUTPUT
echo "" >> $OUTPUT

echo "🔹 Détails réseau cde_net (si existe)" >> $OUTPUT
docker network inspect cde_net >> $OUTPUT 2>&1
echo "" >> $OUTPUT

# -------------------------------
# Containers en cours
# -------------------------------
echo "🔹 Liste des containers" >> $OUTPUT
docker ps -a >> $OUTPUT
echo "" >> $OUTPUT

# -------------------------------
# Ports ouverts critiques
# -------------------------------
echo "🔹 Ports critiques utilisés" >> $OUTPUT
sudo lsof -i -P -n | grep -E "5432|27017|5000|8000|8501|8502|3000|9090" >> $OUTPUT 2>&1
echo "" >> $OUTPUT

echo "======================================" >> $OUTPUT
echo "   FIN DU RAPPORT - FICHIER GENERE    " >> $OUTPUT
echo "======================================" >> $OUTPUT

echo ""
echo "✔ Rapport généré dans : $OUTPUT"

