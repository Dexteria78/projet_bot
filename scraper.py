from config import ARTICLES
import requests
from bs4 import BeautifulSoup

def check_availability(article):
    url = article["url"]
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Vérification pour Cultura
    if "cultura.com" in url:
        status = soup.find("p", class_="stock color-red")
        return False if status and "INDISPONIBLE" in status.get_text(strip=True) else True

    # Vérification pour Fnac
    if "fnac.com" in url:
        status = soup.find("div", class_="f-buyBox-availabilityStatus")
        return False if status and "indisponible" in status.get_text(strip=True) else True

    # Vérification pour Le Repaire du Dragon
    if "lerepairedudragon.fr" in url:
        status = soup.find("span", class_="label label-danger")
        return False if status and "n'est pas en stock" in status.get_text(strip=True) else True

    return False
