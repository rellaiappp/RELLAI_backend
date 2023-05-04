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
    id: Union[str, None] = None
    timestamp: Union[str, None] = None
    quote_id: Union[str, None] = None
    item_name: str
    item_type: str
    item_description: str
    item_unit: str
    item_number: float
    item_unit_price: float
    item_completion: float


class Quote(BaseModel):
    id: Union[str, None] = None
    timestamp: Union[str, None] = None
    creator_id: str
    quote_description: str
    project_id: str
    quote_name: str
    quote_type: str
    quote_validity: str
    items: List[Item] = []
    quote_status: str
    accepted: bool
    total_price: Union[float, None] = None
    quote_completion: Union[float, None] = None



class Project(BaseModel):
    id: Union[int, None] = None
    timestamp: Union[str, None] = None
    creator_id: str
    status: str
    general_info: GeneralInformation
    client_info: Client
    client_mail: str
    total: Union[str,None] = None



class Invite(BaseModel):
    sender_id: str
    project_id: str
    receiver_mail: str
    user_role: str
    accepted: bool

class CompletionRequest(BaseModel):
    id: Union[str, None] = None
    timestamp: Union[int, None] = None
    creator_id: str
    quote: Quote
    quote_id: str
    project_id: str
    note: str
    images: List[str] = []
    accepted: bool
    rejected: bool
