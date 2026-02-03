import time
import requests
import subprocess

API_URL = "http://127.0.0.1:8000/on"

try:
    requests.post(API_URL, json={
        "machine": "PC-MAISON",
        "event": "shutdown"
    }, timeout=0.5)
except Exception:
    pass  # on ignore toute erreur, extinction quoi qu'il arrive

time.sleep(1)

subprocess.run(["shutdown", "/s", "/t", "0"], shell=True)