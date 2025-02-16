from config import ARTICLES
import requests
from bs4 import BeautifulSoup
import pickle
import os

def load_status():
    if os.path.exists("status.pkl"):
        with open("status.pkl", "rb") as f:
            return pickle.load(f)
    return {}

def save_status(status):
    with open("status.pkl", "wb") as f:
        pickle.dump(status, f)

def check_availability(article):
    url = article["url"]
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    if "cultura.com" in url:
        status = soup.find("p", class_="stock color-red")
        text = status.get_text(strip=True).lower() if status else ""
        return text != "indisponible en ligne"

    if "fnac.com" in url:
        status = soup.find("p", {"data-automation-id": "product-availability"})
        text = status.get_text(strip=True).lower() if status else ""
        return text != "stock en ligne épuisé"

    if "lerepairedudragon.fr" in url:
        status = soup.find("span", class_="label label-danger")
        text = status.get_text(strip=True).lower() if status else ""
        return text != "n'est pas en stock"

    return False

previous_status = load_status()

def has_changed(article):
    current = check_availability(article)
    url = article["url"]
    changed = url not in previous_status or previous_status[url] != current
    previous_status[url] = current
    save_status(previous_status)
    return changed and current
