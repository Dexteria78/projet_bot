from config import ARTICLE_URL
import requests
from bs4 import BeautifulSoup

def check_availability():
    response = requests.get(ARTICLE_URL)
    soup = BeautifulSoup(response.content, "html.parser")
    status = soup.find("p", class_="stock color-red")

    if status and "INDISPONIBLE EN LIGNE" in status.get_text(strip=True):
        return False
    else:
        return True if status else False
