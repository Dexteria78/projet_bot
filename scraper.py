from config import ARTICLES
import requests
from bs4 import BeautifulSoup

def check_availability(article):
    url = article["url"]
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    if "cultura.com" in url:
        status = soup.select_one("div#pdp-availability .stock")
        return status is None or "indisponible" not in status.get_text(strip=True).lower()

    if "fnac.com" in url:
        status = soup.select_one("p[data-automation-id='product-availability']")
        return status is None or "épuisé" not in status.get_text(strip=True).lower()

    if "lerepairedudragon.fr" in url:
        status = soup.select_one("span.label.label-danger")
        return status is None or "n'est pas en stock" not in status.get_text(strip=True).lower()

    return False
