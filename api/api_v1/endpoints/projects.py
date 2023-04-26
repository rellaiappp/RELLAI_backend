from fastapi import APIRouter
from pydantic import BaseModel


class Client(BaseModel):
    name: str
    email: str
    phone: str

class SiteInformation(BaseModel):
    address: str
    city: str
    state: str
    zip: str
    type: str
    year_built: int
    floors: int
    area: float
    note: str

class Item(BaseModel):
    id: int | None = None
    name: str
    type: str
    description: str
    unit_of_measure: str
    quantity: int
    unit_price: float

class Quote(BaseModel):
    id: int | None = None
    title: str
    type: str
    items: list[Item]

class Project(BaseModel):
    id: int | None = None
    creator_id: int | None = None
    name: str
    site_information: SiteInformation
    quotes: list[Quote]

router = APIRouter()

@router.post("/")
async def create_project(user_id: int, project: Project):
    return project