from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from security import verify_password, create_access_token, create_refresh_token
import jwt
from dotenv import load_dotenv
import os

from database.database import get_session
from database.crud import get_user_by_email
from sqlmodel import Session

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

route = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


class LoginRequest(BaseModel):
    email: str
    password: str


@route.post("/login")
def login(data: LoginRequest, session: Session = Depends(get_session)):
    print('Tentative de connection pour :', data.email)


    user = get_user_by_email(session, data.email)


    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"user_id": user.id})
    refresh_token = create_refresh_token({"user_id": user.id})

    print('Connection réussie, tokens générés')
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


class RefreshRequest(BaseModel):
    refresh_token: str


@route.post("/refresh")
def refresh(data: RefreshRequest):
    print('Tentative de rafraîchissement du token avec:', data.refresh_token)
    try:
        payload = jwt.decode(data.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Nouveau access token
    new_access_token = create_access_token({"user_id": user_id})
    return {"access_token": new_access_token, "token_type": "bearer"}