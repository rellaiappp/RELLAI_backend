# import firebase_admin
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from firebase_admin import credentials, auth
from pydantic import BaseModel
router = APIRouter()
import traceback



@router.get("/")
async def get_users():
    return {"message":"Users!"}

class User(BaseModel):
    uid: str
    role: str
    mail: str
    name: str

@router.post("/register")
async def register_user(request: Request, user: User):
    try:
        decoded_token = auth.verify_id_token(user.uid)
        uid = decoded_token['uid']
        docref = request.app.db.collection(u'users').document(str(uid))
        result = docref.set({
            u'auth_id': uid,
            u'role': user.role,
            u'mail': user.mail,
            u'name': user.name,
        })
        #request.app.database["users"].insert_one({"uid":user.uid,"role":user.role})
        return {"message":"User created successfully!"}
    except Exception as e:
        traceback.print_exc()
        return {"message":e}
        #raise HTTPException(status_code=400, detail=e)
    