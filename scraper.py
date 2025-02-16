from config import ARTICLES
import requests
from bs4 import BeautifulSoup

def check_availability(article):
    url = article["url"]
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    if "cultura.com" in url:
        status = soup.find("p", class_="stock color-red")
        if status is None:
            return True  # Disparu
        text = status.get_text(strip=True).lower()
        return text != "indisponible en ligne"  # Changé

    if "fnac.com" in url:
        status = soup.find("p", {"data-automation-id": "product-availability"})
        if status is None:
            return True
        text = status.get_text(strip=True).lower()
        return text != "stock en ligne épuisé"

    if "lerepairedudragon.fr" in url:
        status = soup.find("span", class_="label label-danger")
        if status is None:
            return True
        text = status.get_text(strip=True).lower()
        return text != "n'est pas en stock"

    return False

previous_status = {}

def has_changed(article):
    current = check_availability(article)
    url = article["url"]
    if url not in previous_status:
        previous_status[url] = current
        return False
    changed = (previous_status[url] == False and current == True)  # Passe de indisponible à dispo
    previous_status[url] = current
    return changed
