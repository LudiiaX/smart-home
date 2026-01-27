import tinytuya
from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

DEVICE_ID = os.getenv("DEVICE_ID")
DEVICE_IP = os.getenv("DEVICE_IP")
LOCAL_KEY = os.getenv("LOCAL_KEY")

print(DEVICE_ID, DEVICE_IP, LOCAL_KEY)

d = tinytuya.OutletDevice(
    DEVICE_ID,
    DEVICE_IP,
    LOCAL_KEY
)

d.set_version(3.3)

app = FastAPI()

@app.get("/status")
def get_status():
    return d.status()