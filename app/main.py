from fastapi import FastAPI
from api.api_v1.api import router as api_router
import uvicorn
import firebase_admin
import pyrebase
from firebase_admin import credentials, auth
from fastapi.middleware.cors import CORSMiddleware
import json

cred = credentials.Certificate('eeee_service_account_keys.json')
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('../rellai_backend_firebase.json')))
app = FastAPI()

allow_all = ['*']
app.add_middleware(
   CORSMiddleware,
   allow_origins=allow_all,
   allow_credentials=True,
   allow_methods=allow_all,
   allow_headers=allow_all
)


@app.get("/")
async def root():
  return {"message": "Hello World"}

app.include_router(api_router,prefix="/api/v1")

if __name__ == "__main__":
   uvicorn.run("main:app")