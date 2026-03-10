from fastapi import Depends, FastAPI ,Header ,HTTPException

from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from models.prise import Prise, PriseState

import auth

from security import verify_token



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1", "http://192.168.1.19"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.route)

prise = Prise("prise_bureau")

try:
    prise.status = prise.get_status()
except Exception as e:
    print("Erreur lors de l'initialisation du statut de la prise :", e) 



class StatusResponse(BaseModel):
    status: int
    message: str

@app.get("/status", response_model=StatusResponse)
def get_status(payload: dict = Depends(verify_token)):
    try :
        current_status = prise.get_status()
        return {"status": current_status.value, "message": current_status.message}
    except Exception as e:
        return {"status": PriseState.UNKNOWN.value, "message": f"Erreur lors de la récupération du statut : {e}"}
    


class SetStatusRequest(BaseModel):
    state: int

@app.post("/status", response_model=StatusResponse)
def set_status(body: SetStatusRequest, payload: dict = Depends(verify_token)):
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