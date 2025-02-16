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
            return True  # Message disparu
        text = status.get_text(strip=True).lower()
        return "indisponible en ligne" not in text  # Change ou disparition

    if "fnac.com" in url:
        status = soup.find("p", {"data-automation-id": "product-availability"})
        if status is None:
            return True
        text = status.get_text(strip=True).lower()
        return "stock en ligne épuisé" not in text

    if "lerepairedudragon.fr" in url:
        status = soup.find("span", class_="label label-danger")
        if status is None:
            return True
        text = status.get_text(strip=True).lower()
        return "n'est pas en stock" not in text

    return False

previous_status = {}

def has_changed(article):
    current = check_availability(article)
    url = article["url"]
    if url not in previous_status:
        previous_status[url] = current
        return False
    changed = previous_status[url] != current and current  # Change et disponibilité
    previous_status[url] = current
    return changed
