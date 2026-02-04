import requests

API_TOKEN = "0123456789"

headers = {
    "X-API-Key": API_TOKEN,
    "Content-Type": "application/json"
}

API_URL = "http://192.168.1.23:8000/status"

r = requests.get(API_URL, headers=headers)

if r.status_code == 200:
    print("Status API :", r.json())
else:
    print("Erreur :", r.status_code, r.text)