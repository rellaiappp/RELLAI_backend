from api.api_v1.api import router as api_router
import uvicorn
import firebase_admin
from firebase_admin import firestore
import json
from firebase_admin import credentials, auth
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
import ssl

cred = credentials.Certificate('rellai_backend_firebase.json')
firebase = None 

app = FastAPI()

allow_all = ['*']
app.add_middleware(
   CORSMiddleware,
   allow_origins=allow_all,
   allow_credentials=True,
   allow_methods=allow_all,
   allow_headers=allow_all
)

@app.on_event("startup")
async def startup_event():
    firebase_admin.initialize_app(cred)
    app.db = firestore.client()

@app.get("/")
async def root():
  return {"message": "Hello World"}

app.include_router(api_router,prefix="/api/v1")

if __name__ == "__main__":
   uvicorn.run("main:app", host="0.0.0.0", port=8080)
