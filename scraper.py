import time
import requests
from bs4 import BeautifulSoup
from config import DISCORD_WEBHOOK_URL, CHECK_INTERVAL, ARTICLES

def send_discord_message(message):
    payload = {"content": message}
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

def check_availability(article):
    url = article["url"]
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        if "cultura.com" in url:
            status = soup.select_one("div#pdp-availability .stock")
            text = status.get_text(strip=True).lower() if status else "indisponible"
        elif "fnac.com" in url:
            price_element = soup.select_one("span.f-priceBox_price.userPrice.checked")
            if price_element:
                price_text = price_element.get_text(strip=True).replace("€", "").replace(",", ".")
                try:
                    price = float(price_text)
                    if price == 6.99:
                        return True
                except ValueError:
                    return False
            return False
        elif "lerepairedudragon.fr" in url:
            price_element = soup.select_one("span.f-priceBox_price.userPrice.checked")
            if price_element:
                price_text = price_element.get_text(strip=True).replace("€", "").replace(",", ".")
                try:
                    price = float(price_text)
                    if price == 140.00:
                        return True
                except ValueError:
                    return False
            return False
        else:
            return False
    except requests.RequestException as e:
        print(f"Erreur sur {url}: {e}")
        return False

def main():
    send_discord_message("🚀 Le bot Discord surveille plusieurs sites !")
    while True:
        stock_detected = False
        for article in ARTICLES:
            if check_availability(article):
                send_discord_message(f"{article['message']} ({article['url']})")
                stock_detected = True
        if not stock_detected:
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
