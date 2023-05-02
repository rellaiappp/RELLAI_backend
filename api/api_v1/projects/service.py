from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from firebase_admin import credentials, auth
from data_management.projects import ProjectDataManagement
from utils.email import sendConfirmationEmail

def get_projects(request, auth_token):
    try:
        print(auth_token)
        decoded_token = auth.verify_id_token(auth_token)
        uid = decoded_token['uid']
        projects = []
        for doc in request.app.db.collection(u'projects').where(u'creator_id', u'==', uid).stream():
            projects.append(doc.to_dict())
        return {"projects":projects}
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)

def get_invites(request,id):
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
        raise HTTPException(status_code=400, detail=e)

def create_project(request, data):
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