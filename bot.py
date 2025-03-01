import time
import requests
import chromedriver_autoinstaller
from selenium import webdriver
from bs4 import BeautifulSoup
from config import DISCORD_WEBHOOK_URL, CHECK_INTERVAL, ARTICLES

def send_discord_message(message):
    payload = {"content": message}
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

def get_page_source(url):
    # Installer automatiquement ChromeDriver
    chromedriver_autoinstaller.install()

    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium-browser"  # Chemin de Chrome sur Railway
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)  # Attendre le chargement de la page
    html = driver.page_source
    driver.quit()
    return html

def check_availability(article):
    url = article["url"]
    try:
        html = get_page_source(url)
        soup = BeautifulSoup(html, "html.parser")
        
        if "fnac.com" in url:
            print("[DEBUG] Scrapping page Fnac avec Selenium...")
            price_element = soup.select_one("div.f-priceBox__priceLine span.f-priceBox_price")
            if not price_element:
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
    except Exception as e:
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
