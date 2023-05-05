from api.api_v1.api import router as api_router
import uvicorn
from firebase_admin import firestore, credentials, auth, initialize_app
from firebase_admin import exceptions as firebase_exceptions
import firebase_admin
import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
import ssl

cred = credentials.Certificate('rellai_backend_firebase.json')
firebase = firebase_admin.initialize_app(cred)


app = FastAPI()
app.db = firestore.client()

allow_all = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_all,
    allow_credentials=True,
    allow_methods=allow_all,
    allow_headers=allow_all
)


@app.get("/")
async def get_user_projects(request: Request):
    try:
        jwt = request.headers['authorization'].split('bearer ')[1]
        print(jwt)
        decoded_token = auth.verify_id_token(jwt, check_revoked=True)
        return True
    except Exception as e:
        print(e)
        return False
        # raise HTTPException(
        #     status_code=400, detail="Error occurred while fetching projects." + str(e))


@app.get("/")
async def root():
    return {"message": "Hello, World!"}

app.include_router(api_router, prefix="/api/v1")
