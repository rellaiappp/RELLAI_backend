from fastapi import FastAPI
from api.api_v1.api import router as api_router
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import json

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
   uvicorn.run("main:app", host="0.0.0.0", port=8080)