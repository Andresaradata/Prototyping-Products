import os
import requests
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

print("APP_ID:", APP_ID)
print("APP_KEY:", "OK" if APP_KEY else None)

BASE_URL = "https://api.adzuna.com/v1/api/jobs/nl/search/1"

params = {
    "app_id": APP_ID,
    "app_key": APP_KEY,
    "results_per_page": 5,
    "content-type": "application/json"
}

response = requests.get(BASE_URL, params=params)

print("Status code:", response.status_code)

if response.status_code == 200:
    data = response.json()
    print("Total anuncios encontrados:", data.get("count"))
    print("Ejemplo de anuncio:")
    print(data["results"][0]["title"])
else:
    print(response.text)