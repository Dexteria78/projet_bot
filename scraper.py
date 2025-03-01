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
        
        if "fnac.com" in url:
            print("[DEBUG] Scrapping page Fnac...")
            print(soup.prettify()[:1000])  # Afficher un extrait du HTML pour debug
            
            price_element = soup.select_one("div.f-priceBox__priceLine span.f-priceBox_price")
            if not price_element:
                print("[DEBUG] Premier sélecteur de prix échoué, test d'autres sélecteurs...")
                price_element = soup.select_one("span.f-priceBox_price")
            
            if price_element:
                price_text = price_element.get_text(strip=True).replace("€", "").replace(",", ".").replace("\xa0", "")
                print(f"[DEBUG] Prix détecté sur Fnac: {price_text}")
                try:
                    price = float(price_text)
                    if price == 6.99:
                        send_discord_message(f"🔔 L'article est disponible à {price}€ sur Fnac ! ({url})")
                        return True
                except ValueError:
                    print("[ERROR] Impossible de convertir le prix en float")
                    return False
            else:
                print("[DEBUG] Aucun prix détecté sur Fnac")
            return False
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
                stock_detected = True
        if not stock_detected:
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
