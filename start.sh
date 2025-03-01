#!/bin/bash

# Installer les dépendances système
apt-get update && apt-get install -y python3-distutils chromium-browser chromium-driver

# Définir les variables d'environnement pour Selenium
export PATH="/usr/lib/chromium-browser/:$PATH"

# Lancer le bot
python3 bot.py
