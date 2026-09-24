#!/bin/bash
# ==============================================================================
# Script de Déploiement Automatique 1-Clic pour ONIZOUKA SHOP sur o2switch
# Domaine : onizouka.danayaplus.com
# ==============================================================================

set -e

echo "=========================================================="
echo "    DÉPLOIEMENT ONIZOUKA SHOP (o2switch / cPanel)"
echo "=========================================================="

APP_DIR="/home/vuxe8870/repositories/onizukashop"
VENV_DIR="/home/vuxe8870/virtualenv/repositories/onizukashop/3.12"

cd "$APP_DIR" || exit 1

echo ">>> [1/7] Récupération du code et des assets depuis GitHub..."
git pull origin main

echo ">>> [2/7] Configuration de l'environnement (.env)..."
if [ ! -f .env ]; then
    cp .env.production .env
    echo "Fichier .env initialisé depuis .env.production."
fi

echo ">>> [3/7] Activation de l'environnement virtuel Python 3.12..."
source "$VENV_DIR/bin/activate"

echo ">>> [4/7] Installation des dépendances Python..."
pip install --upgrade pip
pip install -r requirements.txt

echo ">>> [5/7] Application des migrations PostgreSQL..."
python manage.py migrate --noinput

echo ">>> [6/7] Chargement des données de démonstration..."
python manage.py loaddata fixtures/demo_data.json || echo "Note : Fixtures déjà chargées ou sautées."

echo ">>> [7/7] Collecte des fichiers statiques (CSS, JS, images)..."
python manage.py collectstatic --noinput

echo ">>> Redémarrage de l'application WSGI Phusion Passenger..."
mkdir -p tmp
touch tmp/restart.txt

echo "=========================================================="
echo "    DÉPLOIEMENT TERMINÉ AVEC SUCCÈS !"
echo "    Boutique : https://onizouka.danayaplus.com"
echo "    ERP Direction : https://onizouka.danayaplus.com/gestion/"
echo "=========================================================="
