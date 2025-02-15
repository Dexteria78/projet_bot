from config import ARTICLES
import requests
from bs4 import BeautifulSoup

def check_availability(article):
    url = article["url"]
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    if "cultura.com" in url:
        status = soup.find("p", class_="stock color-red")
        return not (status and "INDISPONIBLE" in status.get_text(strip=True))

    if "fnac.com" in url:
        status = soup.find("div", class_="f-buyBox-availabilityStatus")
        return not (status and "indisponible" in status.get_text(strip=True))

    if "lerepairedudragon.fr" in url:
        status = soup.find("span", class_="label label-danger")
        return not (status and "n'est pas en stock" in status.get_text(strip=True))

    return False
