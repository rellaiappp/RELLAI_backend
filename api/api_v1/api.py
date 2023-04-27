from fastapi import APIRouter
from .endpoints import users
from .endpoints import projects

router = APIRouter()
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(projects.router, prefix="/projects", tags=["Projects"])