from config import ARTICLES
import requests
from bs4 import BeautifulSoup

def check_availability(article):
    url = article["url"]
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    if "cultura.com" in url:
        status = soup.find("p", class_="stock color-red")
        return status is None or "INDISPONIBLE" not in status.get_text(strip=True)

    if "fnac.com" in url:
        status = soup.find("div", class_="f-buyBox-availabilityStatus")
        return status is not None and "disponible" in status.get_text(strip=True).lower()

    if "lerepairedudragon.fr" in url:
        status = soup.find("span", class_="label label-danger")
        return status is None or "n'est pas en stock" not in status.get_text(strip=True)

    return False
