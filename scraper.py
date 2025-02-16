from config import ARTICLES
import requests
from bs4 import BeautifulSoup

previous_status = {}

def check_availability(article):
    url = article["url"]
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    if "cultura.com" in url:
        status = soup.select_one("div#pdp-availability .stock")
        text = status.get_text(strip=True).lower() if status else ""

    elif "fnac.com" in url:
        status = soup.select_one("p[data-automation-id='product-availability']")
        text = status.get_text(strip=True).lower() if status else ""

    elif "lerepairedudragon.fr" in url:
        status = soup.select_one("span.label.label-danger")
        text = status.get_text(strip=True).lower() if status else ""

    else:
        return False

    previous = previous_status.get(url)
    previous_status[url] = text

    return previous is not None and text != previous
