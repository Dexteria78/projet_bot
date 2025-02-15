import time
import requests
from scraper import check_availability
from config import DISCORD_WEBHOOK_URL, CHECK_INTERVAL, ARTICLES

def send_discord_message(message):
    payload = {"content": message}
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

def main():
    send_discord_message("🚀 Le bot Discord surveille plusieurs sites !")
    while True:
        for article in ARTICLES:
            if check_availability(article):
                send_discord_message(f"{article['message']} ({article['url']})")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
