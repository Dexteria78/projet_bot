#!/bin/bash

# Mettre à jour les paquets et installer Chrome et ChromeDriver
apt-get update && apt-get install -y wget unzip curl
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb

# Définir les variables d'environnement pour Selenium
export CHROME_BIN="/usr/bin/google-chrome"
export PATH="$PATH:/usr/bin/"

# Installer ChromeDriver automatiquement
python3 -m pip install --upgrade chromedriver-autoinstaller

# Lancer le bot
python3 bot.py
