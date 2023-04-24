from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from firebase_admin import credentials, auth

router = APIRouter()

@router.get("/")
async def get_users():
    return {"message":"Users!"}

def check_token(token):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token['uid']
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router.post("/")
async def create_user(request: Request):
    token = request.headers['Authorization']
    uid = check_token(token)
    return uid
