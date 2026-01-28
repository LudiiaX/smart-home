import tinytuya
from fastapi import Depends, FastAPI ,Header ,HTTPException
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()

DEVICE_ID = os.getenv("DEVICE_ID")
DEVICE_IP = os.getenv("DEVICE_IP")
LOCAL_KEY = os.getenv("LOCAL_KEY")
API_TOKEN = os.getenv("API_TOKEN")

d = tinytuya.OutletDevice(
    DEVICE_ID,
    DEVICE_IP,
    LOCAL_KEY
)


DESKTOP_STATUS = 0


d.set_version(3.3)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def auth(x_api_key: str = Header(...)):
    if x_api_key != API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

def plug_status():
    data = d.status()
    if data['dps']['1'] == True:
        return {"status": 1, "message": "Prise allumée."}
    elif data['dps']['1'] == False:
        DESKTOP_STATUS = 0
        return {"status": 0, "message": "Prise éteinte."}
    else :
        return {"status": -1, "message": "Erreur lors de la récupération du statut de la prise."}

class StatusResponse(BaseModel):
    status: int
    message: str


@app.get("/status",
         response_model=StatusResponse,
         dependencies=[Depends(auth)]
        )
def get_status():
    print(d.status())
    if DESKTOP_STATUS == 1:
        return {"status": 2, "message": "Ordinateur en marche."}
    else:
        return plug_status()

class OnOffResponse(BaseModel):
    status: int
    message: str


@app.get("/on",
         response_model=OnOffResponse,
         dependencies=[Depends(auth)]
        )
def on():
    response = d.turn_on()
    if response['dps']['1'] == True: 
        return {"status": 1, "message": "Prise allumée."}
    else :
        return {"status": -1, "message": "Erreur lors de l'allumage de la prise."}

@app.get("/off",
         response_model=OnOffResponse,
         dependencies=[Depends(auth)]
        )
def off():
    response = d.turn_off()
    if response['dps']['1'] == False: 
        return {"status": 0, "message": "Prise éteinte."}
    else :
        return {"status": -1, "message": "Erreur lors de l'extinction de la prise."}