from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from firebase_admin import credentials, auth
import traceback
from api.api_v1.endpoints.project_model import Project
from api.api_v1.endpoints.functions import sendConfirmationEmail


router = APIRouter()

@router.get("/data")
async def get_user_projects(request: Request,auth_token: str):
    try:
        print(auth_token)
        decoded_token = auth.verify_id_token(auth_token)
        uid = decoded_token['uid']
        projects = []
        for doc in request.app.db.collection(u'projects').where(u'creator_id', u'==', uid).stream():
            projects.append(doc.to_dict())
        return {"projects":projects}
    except Exception as e:
        traceback.print_exc()
        return {"message":e}
        #raise HTTPException(status_code=400, detail=e)



@router.post("/create")
async def create_project(request: Request, data: Project):
    try:
        print(data)

        decoded_token = auth.verify_id_token(data.creator_id)
        uid = decoded_token['uid']
        print(uid)
        project = {
            u'creator_id': uid,
            u'general_info': dict(data.general_info),
            u'client': dict(data.client_info)
        }
        doc_ref = request.app.db.collection(u'projects').add(project)
        print(sendConfirmationEmail(data.client_info.email,doc_ref[1].id))
        
        #request.app.database["users"].insert_one({"uid":user.uid,"role":user.role})
        return {"message":"User created successfully!"}
    except Exception as e:
        #traceback.print_exc()
        #return {"message":e}
        raise HTTPException(status_code=400, detail=e)