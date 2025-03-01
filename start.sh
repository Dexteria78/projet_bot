#!/bin/bash

# Mettre à jour les paquets et installer Chrome et ChromeDriver
apt-get update && apt-get install -y chromium-browser chromium-driver

# Définir les variables d'environnement pour Selenium
export CHROME_BIN="/usr/bin/chromium-browser"
export PATH="/usr/lib/chromium-browser/:$PATH"

# Lancer le bot
python3 bot.py
