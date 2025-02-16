from config import ARTICLES
import requests
from bs4 import BeautifulSoup

previous_status = {}

def check_availability(article):
    url = article["url"]
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    if "cultura.com" in url:
        text = soup.select_one("div#pdp-availability .stock")
        text = text.get_text(strip=True).lower() if text else ""

    elif "fnac.com" in url:
        text = soup.select_one("p[data-automation-id='product-availability']")
        text = text.get_text(strip=True).lower() if text else ""

    elif "lerepairedudragon.fr" in url:
        text = soup.select_one("span.label.label-danger")
        text = text.get_text(strip=True).lower() if text else ""

    else:
        return False

    previous = previous_status.get(url)
    previous_status[url] = text

    return previous is not None and text != previous

# Pour tester : modifiez temporairement le texte récupéré dans la fonction pour simuler un changement.
