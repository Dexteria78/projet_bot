import time
import requests
from scraper import check_availability
from config import DISCORD_WEBHOOK_URL, CHECK_INTERVAL, ARTICLE_URL

def send_discord_message(message):
    payload = {"content": message}
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

def main():
    send_discord_message("🚀 Le bot Discord est bien en ligne sur Railway et surveille l'article !")
    while True:
        if check_availability():
            send_discord_message(f"L'article est disponible ! Dépêche-toi : {ARTICLE_URL}")
            break
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
