from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from firebase_admin import credentials, auth
import traceback
from api.api_v1.endpoints.project_model import Project, Invite, Quote
from api.api_v1.endpoints.functions import sendConfirmationEmail
from firebase_admin import firestore
import time
from data_management.projects import ProjectDataManagement


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
        #return {"message":e}
        raise HTTPException(status_code=400, detail=e)

@router.get("invites/data")
async def get_user_projects(request: Request,id: str):
    try:
        jwt = request.headers['Authorization'].split('bearer ')[1]
        decoded_token = auth.verify_id_token(jwt)
        assert decoded_token['uid'] == id

        uid = decoded_token['uid']
        projects = []
        for doc in request.app.db.collection(u'projects').where(u'creator_id', u'==', uid).stream():
            projects.append(doc.to_dict())
        return {"projects":projects}
    except Exception as e:
        traceback.print_exc()
        #return {"message":e}
        raise HTTPException(status_code=400, detail=e)




@router.post("/create")
async def create_project(request: Request, data: Project):
    try:
        print(request.headers['Authorization'])
        jwt = request.headers['Authorization'].split('bearer ')[1]
        decoded_token = auth.verify_id_token(jwt)
        assert decoded_token['uid'] == data.creator_id
        ProjectDataManagement.create_project(data,request.app.db)
        print(sendConfirmationEmail(data.client_info.email,data.client_info.email))
        return {"message":"Project created successfully!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)
    

@router.get("/invites/data")
async def get_invites(request: Request,id: str):
    try: 
        print(request.headers['Authorization'])
        jwt = request.headers['Authorization'].split('bearer ')[1]
        decoded_token = auth.verify_id_token(jwt)
        assert decoded_token['uid'] == id
        result = ProjectDataManagement.get_project_invitations(id, request.app.db)
        print(result)
        return {"projects":result}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)



@router.post("/invites/{invite_id}/accept")
async def accept_invite(request: Request,invite_id: str):
    try: 
        print(invite_id)
        jwt = request.headers['Authorization'].split('bearer ')[1]
        decoded_token = auth.verify_id_token(jwt)
        id = decoded_token['uid']
        result = ProjectDataManagement.accept_invitation(invite_id,id, request.app.db)
        return {"result":result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)


@router.post("/invites/{invite_id}/reject")
async def reject_invite(request: Request,invite_id: str):
    try: 
        print(invite_id)
        jwt = request.headers['Authorization'].split('bearer ')[1]
        decoded_token = auth.verify_id_token(jwt)
        id = decoded_token['uid']
        result = ProjectDataManagement.accept_invitation(invite_id,id, request.app.db)
        return {"result":result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)

@router.post("/quote/create")
async def create_quote(request: Request, data: Quote):
    try:
        print(request.headers['Authorization'])
        jwt = request.headers['Authorization'].split('bearer ')[1]
        decoded_token = auth.verify_id_token(jwt)
        assert decoded_token['uid'] == data.creator_id
        ProjectDataManagement.create_quote(data,request.app.db)
        return {"message":"Project created successfully!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)