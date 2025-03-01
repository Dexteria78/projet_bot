#!/bin/bash

# Mettre à jour les paquets et installer les dépendances nécessaires
apt-get update && apt-get install -y python3-distutils chromium-browser chromium-driver

# Définir les variables d'environnement pour Selenium
export PATH="/usr/lib/chromium-browser/:$PATH"

# Installer ChromeDriver automatiquement
python3 -m pip install --upgrade chromedriver-autoinstaller

# Lancer le bot
python3 bot.py
