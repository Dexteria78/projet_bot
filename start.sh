#!/bin/bash

# Installer Chrome et ChromeDriver sur Railway
apt-get update && apt-get install -y chromium-browser chromium-driver

# Lancer le bot
python3 bot.py
