import requests

API_TOKEN = "0123456789"

headers = {
    "X-API-Key": API_TOKEN,
    "Content-Type": "application/json"
}

API_URL = "http://127.0.0.1:8000/status"

r = requests.post(API_URL, headers=headers, json={"state": 0})

if r.status_code == 200:
    print("Status API :", r.json())
else:
    print("Erreur :", r.status_code, r.text)



r = requests.get(API_URL, headers=headers)

if r.status_code == 200:
    print("Status API :", r.json())
else:
    print("Erreur :", r.status_code, r.text)




r = requests.post(API_URL, headers=headers, json={"state": 1})

if r.status_code == 200:
    print("Status API :", r.json())
else:
    print("Erreur :", r.status_code, r.text)




r = requests.get(API_URL, headers=headers)

if r.status_code == 200:
    print("Status API :", r.json())
else:
    print("Erreur :", r.status_code, r.text)




r = requests.post(API_URL, headers=headers, json={"state": 2})

if r.status_code == 200:
    print("Status API :", r.json())
else:
    print("Erreur :", r.status_code, r.text)


r = requests.get(API_URL, headers=headers)

if r.status_code == 200:
    print("Status API :", r.json())
else:
    print("Erreur :", r.status_code, r.text)
