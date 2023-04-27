from pydantic import BaseModel

class Client(BaseModel):
    full_name: str
    email: str
    phone: str

class SiteInformation(BaseModel):
    address: str
    city: str
    region: str
    year_built: str
    floor: str
    area: str

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
    creator_id: str
    status: str
    general_info: SiteInformation
    client_info: Client
