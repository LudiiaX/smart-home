import tinytuya
from fastapi import Depends, FastAPI ,Header ,HTTPException, WebSocket, WebSocketDisconnect
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
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

clients = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()


    token = websocket.headers.get("x-api-key")
    if token != API_TOKEN:
        await websocket.close(code=1008)
        return


    clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            s = d.status()
            if s['dps']['1'] == True:
                await broadcast_status({
                "status": 1,
                "message": "Prise allumée."
                })
            elif s['dps']['1'] == False:
                await broadcast_status({
                "status": 0,
                "message": "Prise éteinte."
                })
            else :
                await broadcast_status({
                "status": -1,
                "message": "Erreur lors de la récupération du statut de la prise."
                })
    except WebSocketDisconnect:
        clients.remove(websocket)


async def broadcast_status(status: dict):
    for ws in list(clients):
        await ws.send_text(json.dumps({
            "type": "status_update",
            "status": status["status"],
            "message": status["message"]
        }))


class StatusResponse(BaseModel):
    status: int
    message: str

def auth(x_api_key: str = Header(...)):
    if x_api_key != API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/status",
         response_model=StatusResponse,
         dependencies=[Depends(auth)]
        )
async def get_status():
    s = d.status()
    if s['dps']['1'] == True:
        await broadcast_status({
                "status": 1,
                "message": "Prise allumée."
                })
        return {"status": 1, "message": "Prise allumée."}
    elif s['dps']['1'] == False:
        await broadcast_status({
                "status": 0,
                "message": "Prise éteinte."
                })
        return {"status": 0, "message": "Prise éteinte."}
    else:
        await broadcast_status({
                "status": -1,
                "message": "Erreur lors de la récupération du statut de la prise."
                })
        return {"status": -1, "message": "Erreur lors de la récupération du statut de la prise."}
    

class OnOffResponse(BaseModel):
    status: int
    message: str

@app.get("/on",
         response_model=OnOffResponse,
         dependencies=[Depends(auth)]
        )
async def on():
    response = d.turn_on()
    if response['dps']['1'] == True:
        await broadcast_status({
                "status": 1,
                "message": "Prise allumée."
            })
        return {"status": 1, "message": "Prise allumée."}
    else :
        await broadcast_status({
            "status": -1,
            "message": "Erreur lors de la récupération du statut de la prise."
            })
        return {"status": -1, "message": "Erreur lors de l'allumage de la prise."}
