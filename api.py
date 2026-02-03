from fastapi import Depends, FastAPI ,Header ,HTTPException
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from models.prise import Prise, PriseState

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

prise = Prise("prise_bureau")

try:
    prise.status = prise.get_status()
except Exception as e:
    print("Erreur lors de l'initialisation du statut de la prise :", e) 



def auth(x_api_key: str = Header(...)):
    if x_api_key != API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")


class StatusResponse(BaseModel):
    status: int
    message: str

@app.get("/status",
         response_model=StatusResponse,
         dependencies=[Depends(auth)]
        )
def get_status():
    try :
        current_status = prise.get_status()
        return {"status": current_status.value, "message": current_status.message}
    except Exception as e:
        return {"status": PriseState.UNKNOWN.value, "message": f"Erreur lors de la récupération du statut : {e}"}
    


class SetStatusRequest(BaseModel):
    state: int

@app.post("/status",
            response_model=StatusResponse,
            dependencies=[Depends(auth)]
            )
def set_status(body: SetStatusRequest):
    print('test', body.state)
    try:
        desired_status = PriseState(body.state)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid status value")

    result = prise.set_status(desired_status)
    print('result', result)
    if isinstance(result, dict):
        return result
    else:
        raise HTTPException(status_code=500, detail="Failed to set status")