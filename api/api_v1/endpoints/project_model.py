from pydantic import BaseModel
from typing import Union
from typing import List

class Client(BaseModel):
      nome: str
      email: str
      numero_cellulare: str

class GeneralInformation(BaseModel):
      nome_progetto: str
      tipologia_abitazione: str
      eta_edificio: str
      metri_quadrati: str
      tipo_intervento: str

class Item(BaseModel):
    id: Union[int, None] = None
    timestamp: Union[str, None] = None
    quote_id: Union[str, None] = None
    item_name: str
    item_type: str
    item_description: str
    item_unit: str
    item_number: int
    item_unit_price: float
    Item_completion: int


class Quote(BaseModel):
    id: Union[int, None] = None
    timestamp: Union[str, None] = None
    creator_id: str
    project_id: str
    quote_name: str
    quote_type: str
    quote_validity: str
    items: List[Item]
    quote_type: str
    quote_status: str
    accepted: bool

class CompletitionRequest(BaseModel):
    id: Union[int, None] = None
    timestamp: Union[str, None] = None
    creator_id: str
    quote_id: str
    items: List[Item]
    note: str
    images: List[str]
     

    

class Project(BaseModel):
    creator_id: str
    status: str
    general_info: GeneralInformation
    client_info: Client
    client_mail: str

class Invite(BaseModel):
    sender_id: str
    project_id: str
    receiver_mail: str
    user_role: str
    accepted: bool

