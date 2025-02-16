from config import ARTICLES
import requests
from bs4 import BeautifulSoup

def check_availability(article):
    url = article["url"]
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    if "cultura.com" in url:
        status = soup.find("p", class_="stock color-red")
        return status is None or "indisponible" not in status.get_text(strip=True).lower()

    if "fnac.com" in url:
        status = soup.find("p", {"data-automation-id": "product-availability"})
        return status is not None and "Stock en ligne épuisé" not in status.get_text(strip=True).lower()

    if "lerepairedudragon.fr" in url:
        status = soup.find("span", class_="label label-danger")
        return status is not None and "n'est pas en stock" in status.get_text(strip=True)

    return False
