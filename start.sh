#!/bin/bash

# Met à jour les paquets et installe Chromium et ChromeDriver
apt-get update && apt-get install -y chromium-browser chromium-driver

# Définir les variables d'environnement pour Selenium
export PATH="/usr/lib/chromium-browser/:$PATH"

# Lancer le bot
python3 bot.py
